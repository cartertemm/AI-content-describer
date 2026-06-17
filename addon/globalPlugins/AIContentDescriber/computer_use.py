import base64
import logging
import math
import queue
import threading
import time
from io import BytesIO

log = logging.getLogger(__name__)

import api
import winUser
import screenBitmap
import ui
import synthDriverHandler
import tones
import wx

import dependency_checker
dependency_checker.expand_path()
from PIL import Image


def _on_main_thread(fn):
	"""Schedule fn() on the wx main thread. A background thread may schedule a UI update just
	as the user closes the dialog, so by the time fn() runs the window can already be destroyed;
	calling into a dead wx object raises RuntimeError, which we catch and log instead of letting
	it surface as a noisy traceback."""
	def _do():
		try:
			fn()
		except RuntimeError:
			log.debug("computer use: skipped a main-thread UI call, window already gone", exc_info=True)
	wx.CallAfter(_do)


ANNOUNCE_TIMEOUT_SECONDS = 10
TYPE_PREVIEW_MAX_CHARS = 40
# Above this length, paste the text instead of synthesizing a keystroke per character.
PASTE_TYPE_THRESHOLD_CHARS = 512

# Sent to the model on every computer-use turn.
# Not currently translated
SYSTEM_PROMPT = (
	"You are controlling a Windows computer on behalf of a blind user who relies on the NVDA "
	"screen reader and cannot see the screen. You are their trusted eyes and hands, so you must "
	"be careful and deliberate.\n\n"
	"Each screenshot shows only the currently focused foreground window. Coordinates are pixels "
	"from the top-left of the screenshot. You will be told which app and window are focused in "
	"each turn. Keyboard and mouse input will be sent to the currently focused window.\n\n"
	"Work one step at a time. After each action, look at the next screenshot and confirm it did "
	"what you expected before continuing. Do not assume an action succeeded. If the focused window "
	"changed to something you did not expect, stop and reassess instead of pushing on. If you are "
	"stuck or the task is ambiguous, stop and ask the user rather than guessing."
)


def on_control_start():
	"""Beep signalling the model has taken control: session start or resume."""
	tones.beep(1000, 300)


def on_control_pause():
	"""Beep signalling the model has stopped touching the machine while the session is
	still alive because the user paused, or the model wants input."""
	tones.beep(108, 300)


def _announce_and_wait(text):
	done = threading.Event()
	def _on_done(**kwargs):
		done.set()
	# HandlerRegistrar stores only a weak reference; _on_done must stay alive
	# for the duration of this call. The stack frame keeps it alive while we block.
	synthDriverHandler.synthDoneSpeaking.register(_on_done)
	try:
		ui.message(text)
		# synthDoneSpeaking fires for any speech, not specifically this utterance.
		done.wait(timeout=ANNOUNCE_TIMEOUT_SECONDS)
	finally:
		synthDriverHandler.synthDoneSpeaking.unregister(_on_done)


def _calculate_scale(w, h, max_long_edge=None, max_pixels=None):
	"""Return the scale factor satisfying both the long-edge and pixel-area limits."""
	scale = 1.0
	if max_long_edge is not None:
		long_edge = max(w, h)
		if long_edge > max_long_edge:
			scale = min(scale, max_long_edge / long_edge)
	if max_pixels is not None:
		pixels = w * h
		if pixels > max_pixels:
			scale = min(scale, math.sqrt(max_pixels / pixels))
	return scale


def _focus_metadata(obj, width, height):
	"""Build the focused-window metadata for a capture.
	This is sent to the model as part of every computer-use request."""
	app_name = ""
	app_version = ""
	window_title = ""
	if obj is not None:
		try:
			app_module = getattr(obj, "appModule", None)
			if app_module is not None:
				app_name = getattr(app_module, "appName", "") or ""
				app_version = getattr(app_module, "productVersion", "") or ""
			window_title = getattr(obj, "name", "") or ""
		except Exception:
			log.debug("computer use: could not read focus metadata", exc_info=True)
	return {
		"app_name": app_name,
		"app_version": app_version,
		"window_title": window_title,
		"width": width,
		"height": height,
	}


def format_focus_context(focus):
	"""Render the focus metadata that accompanies each screenshot, so the model knows which
	window it is looking at and does not send input on unexpected focus changes."""
	app = focus.get("app_name") or "unknown"
	version = focus.get("app_version") or ""
	if version:
		app = f"{app} {version}"
	return (
		f"Focused app: {app}\n"
		f"Focused window: {focus.get('window_title') or 'unknown'}\n"
		f"Screenshot size: {focus.get('width')}x{focus.get('height')}"
	)


class Capture:
	"""Captures the live foreground window as a scaled base64 PNG.

	`resolve_target` is a callable returning (hwnd, obj) for the frame to capture: the current
	foreground window, or a fallback when the foreground is one of our own dialogs. `obj` is the
	NVDA foreground object used for focus metadata, or None on fallback."""

	def __init__(self, resolve_target, max_long_edge=None, max_pixels=None):
		self._resolve_target = resolve_target
		self._max_long_edge = max_long_edge
		self._max_pixels = max_pixels
		self._scale = 1.0
		self._win_x = 0
		self._win_y = 0

	def capture(self):
		"""Returns (b64_png_str, api_w, api_h, focus_dict)."""
		hwnd, obj = self._resolve_target()
		rect = winUser.getClientRect(hwnd)
		cap_w = rect.right - rect.left
		cap_h = rect.bottom - rect.top
		self._win_x, self._win_y = winUser.ClientToScreen(hwnd, 0, 0)
		self._scale = _calculate_scale(cap_w, cap_h, self._max_long_edge, self._max_pixels)
		api_w = max(1, int(cap_w * self._scale))
		api_h = max(1, int(cap_h * self._scale))
		buf = screenBitmap.ScreenBitmap(api_w, api_h).captureImage(
			self._win_x, self._win_y, cap_w, cap_h
		)
		img = Image.frombuffer("RGB", (api_w, api_h), buf, "raw", "BGRX", 0, 1)
		out = BytesIO()
		img.save(out, format="PNG")
		b64 = base64.b64encode(out.getvalue()).decode("ascii")
		focus = _focus_metadata(obj, api_w, api_h)
		return b64, api_w, api_h, focus

	def to_screen(self, rx, ry):
		"""Convert API-space coordinates to physical screen coordinates for the last frame."""
		return int(rx / self._scale) + self._win_x, int(ry / self._scale) + self._win_y


def describe_action(action):
	"""Return a short user-facing description of a computer-use action."""
	action_desc = action.get("type", "unknown")
	if "x" in action and "y" in action:
		action_desc += f" at ({action['x']}, {action['y']})"
	if "text" in action:
		action_desc += f": {action['text'][:TYPE_PREVIEW_MAX_CHARS]}"
	if "key" in action:
		action_desc += f": {action['key']}"
	return action_desc


def safety_check_messages(action):
	"""Return displayable messages from API-issued safety checks."""
	messages = [sc.get("message") or sc.get("code", "") for sc in action.get("safety_checks", [])]
	return [m for m in messages if m]


def format_action_result(action, detail, status="ok"):
	return f"{action.get('type', '')} | {detail} | {status}"


_active_session = None


def get_active_session():
	"""Return the one running ComputerUseSession, or None.

	Note: It is only possible to have one session running at a time."""
	return _active_session


def _set_active_session(session):
	global _active_session
	_active_session = session


def _clear_active_session(session):
	global _active_session
	if _active_session is session:
		_active_session = None


class ActionRunner:
	"""Executes model-issued actions using NVDA's winUser module."""

	def __init__(self, cancel_event=None, pause_event=None):
		self._cancel_event = cancel_event
		self._pause_event = pause_event

	def _aborted(self):
		"""True when the session was cancelled or paused, so long actions stop mid-flight."""
		return ((self._cancel_event is not None and self._cancel_event.is_set())
			or (self._pause_event is not None and self._pause_event.is_set()))

	_VK_MAP = {
		"enter": 0x0D, "return": 0x0D, "tab": 0x09, "escape": 0x1B, "esc": 0x1B,
		"space": 0x20, "backspace": 0x08, "delete": 0x2E,
		"up": 0x26, "down": 0x28, "left": 0x25, "right": 0x27,
		"home": 0x24, "end": 0x23, "pageup": 0x21, "pagedown": 0x22,
		"f1": 0x70, "f2": 0x71, "f3": 0x72, "f4": 0x73,
		"f5": 0x74, "f6": 0x75, "f7": 0x76, "f8": 0x77,
		"f9": 0x78, "f10": 0x79, "f11": 0x7A, "f12": 0x7B,
		"win": 0x5B, "windows": 0x5B,
	}
	_MOD_MAP = {"ctrl": 0x11, "control": 0x11, "shift": 0x10, "alt": 0x12, "win": 0x5B}

	def execute(self, action):
		"""Execute one action dict; return a compact result string."""
		t = action.get("type", "")
		try:
			if t == "move":
				self._move(action["x"], action["y"])
				return format_action_result(action, f"({action['x']}, {action['y']})")
			elif t == "left_click":
				self._click(action["x"], action["y"], "left")
				return format_action_result(action, f"({action['x']}, {action['y']})")
			elif t == "right_click":
				self._click(action["x"], action["y"], "right")
				return format_action_result(action, f"({action['x']}, {action['y']})")
			elif t == "middle_click":
				self._click(action["x"], action["y"], "middle")
				return format_action_result(action, f"({action['x']}, {action['y']})")
			elif t == "double_click":
				self._click(action["x"], action["y"], "left")
				time.sleep(0.05)
				self._click(action["x"], action["y"], "left")
				return format_action_result(action, f"({action['x']}, {action['y']})")
			elif t == "triple_click":
				for _ in range(3):
					if self._aborted():
						break
					self._click(action["x"], action["y"], "left")
					time.sleep(0.05)
				return format_action_result(action, f"({action['x']}, {action['y']})")
			elif t == "left_click_drag":
				self._drag(action["startX"], action["startY"], action["endX"], action["endY"])
				return format_action_result(action, f"({action['startX']},{action['startY']})->({action['endX']},{action['endY']})")
			elif t == "scroll":
				_announce_and_wait("Scrolling...")
				self._scroll(action["x"], action["y"], action.get("direction", "down"), action.get("amount", 3))
				return format_action_result(action, f"({action['x']}, {action['y']}) {action.get('direction', 'down')} {action.get('amount', 3)}")
			elif t == "key":
				self._key(action["key"])
				return format_action_result(action, action["key"])
			elif t == "type":
				preview = action["text"][:TYPE_PREVIEW_MAX_CHARS]
				_announce_and_wait(f"Typing {preview}")
				self._type_text(action["text"])
				return format_action_result(action, preview)
			elif t == "wait":
				time.sleep(0.5)
				_announce_and_wait("Waiting for 500 MS...")
				return format_action_result(action, "500ms")
			elif t == "screenshot":
				_announce_and_wait("Taking screenshot...")
				return format_action_result(action, "(handled by loop)")
			else:
				return format_action_result(action, "(unknown)", "skipped")
		except Exception as e:
			log.error("computer use: action %r failed", action.get("type"), exc_info=True)
			return format_action_result(action, "error", e)

	def _move(self, x, y):
		winUser.setCursorPos(x, y)

	def _click(self, x, y, button):
		down = {"left": winUser.MOUSEEVENTF_LEFTDOWN, "right": winUser.MOUSEEVENTF_RIGHTDOWN, "middle": winUser.MOUSEEVENTF_MIDDLEDOWN}
		up = {"left": winUser.MOUSEEVENTF_LEFTUP, "right": winUser.MOUSEEVENTF_RIGHTUP, "middle": winUser.MOUSEEVENTF_MIDDLEUP}
		winUser.setCursorPos(x, y)
		winUser.mouse_event(down[button], 0, 0, 0, 0)
		winUser.mouse_event(up[button], 0, 0, 0, 0)

	def _drag(self, sx, sy, ex, ey):
		winUser.setCursorPos(sx, sy)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
		winUser.setCursorPos(ex, ey)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

	def _scroll(self, x, y, direction, amount):
		winUser.setCursorPos(x, y)
		if direction in ("up", "down"):
			delta = winUser.WHEEL_DELTA * amount * (1 if direction == "up" else -1)
			winUser.mouse_event(winUser.MOUSEEVENTF_WHEEL, 0, 0, delta, 0)
		else:
			delta = winUser.WHEEL_DELTA * amount * (1 if direction == "right" else -1)
			winUser.mouse_event(winUser.MOUSEEVENTF_HWHEEL, 0, 0, delta, 0)

	def _key(self, key):
		parts = key.lower().split("+")
		# Empty main_key means the intended key is the literal "+" (e.g. "ctrl++")
		main_key = parts[-1].strip() or "+"
		mod_tokens = [p.strip() for p in parts[:-1] if p.strip()]
		unknown = [t for t in mod_tokens if t not in self._MOD_MAP]
		if unknown:
			raise ValueError(f"unknown modifier(s): {', '.join(unknown)}")
		modifiers = [self._MOD_MAP[t] for t in mod_tokens]
		for vk in modifiers:
			winUser.keybd_event(vk, 0, 0, 0)
		main_vk = self._VK_MAP.get(main_key)
		extra_shift = False
		if main_vk is None and main_key:
			try:
				shift_state, main_vk = winUser.VkKeyScanEx(main_key[0], 0)
				if shift_state & 0x01 and self._MOD_MAP["shift"] not in modifiers:
					extra_shift = True
					winUser.keybd_event(self._MOD_MAP["shift"], 0, 0, 0)
			except LookupError:
				pass
		if main_vk is not None:
			winUser.keybd_event(main_vk, 0, 0, 0)
			winUser.keybd_event(main_vk, 0, winUser.KEYEVENTF_KEYUP, 0)
		if extra_shift:
			winUser.keybd_event(self._MOD_MAP["shift"], 0, winUser.KEYEVENTF_KEYUP, 0)
		for vk in reversed(modifiers):
			winUser.keybd_event(vk, 0, winUser.KEYEVENTF_KEYUP, 0)

	def _type_text(self, text):
		# Long strings are slow to synthesize a keystroke at a time, so paste them. Either method can fail though.
		# For instance, paste needs a control that accepts ctrl+v, and per-character typing can
		# drop keys on slower machines. This is why we fall back to the other if the first one doesn't work.
		# todo: Handle the unlikely case where text can be inputted partially, then fail, then be pasted, thereby duplicating data.
		if len(text) > PASTE_TYPE_THRESHOLD_CHARS:
			if not self._paste_text(text):
				self._type_chars(text)
		else:
			if not self._type_chars(text):
				self._paste_text(text)

	def _type_chars(self, text):
		"""Type the text one synthesized keystroke per character. Returns False if it failed."""
		try:
			for ch in text:
				if self._aborted():
					break
				if ch == "\n":
					winUser.keybd_event(self._VK_MAP["enter"], 0, 0, 0)
					winUser.keybd_event(self._VK_MAP["enter"], 0, winUser.KEYEVENTF_KEYUP, 0)
				else:
					cp = ord(ch)
					winUser.keybd_event(0, cp, winUser.KEYEVENTF_UNICODE, 0)
					winUser.keybd_event(0, cp, winUser.KEYEVENTF_UNICODE | winUser.KEYEVENTF_KEYUP, 0)
				time.sleep(0.005)
			return True
		except Exception:
			log.debug("computer use: direct typing failed", exc_info=True)
			return False

	def _paste_text(self, text):
		"""Set the clipboard and send ctrl+v, restoring the prior contents. Returns False if it failed."""
		try:
			with winUser.openClipboard():
				prior = winUser.getClipboardData(winUser.CF_UNICODETEXT)
			with winUser.openClipboard():
				winUser.setClipboardData(winUser.CF_UNICODETEXT, text)
			self._key("ctrl+v")
			# Brief delay to ensure control+v was actually pressed and released
			time.sleep(0.1)
			with winUser.openClipboard():
				winUser.setClipboardData(winUser.CF_UNICODETEXT, prior if prior is not None else "")
			return True
		except Exception:
			log.error("computer use: clipboard paste failed", exc_info=True)
			return False


class ComputerUseSession:
	"""Orchestrates the agentic control loop on a background thread."""

	def __init__(self, service, hwnd, request_approval=None, parent=None):
		self._service = service
		self._hwnd = hwnd
		self._target_hwnd = hwnd
		self._request_approval = request_approval
		self._cancel_event = threading.Event()
		self._pause_event = threading.Event()
		self._inject_queue = queue.Queue()
		self._approve_all = False
		self._thread = None
		self._dialog_visible = False
		self._max_long_edge = getattr(service, "_capture_max_long_edge", None)
		self._max_pixels = getattr(service, "_capture_max_pixels", None)
		# Imported lazily (not at module top) to break the computer_use <-> computer_use_dialogs
		# import cycle: the dialog module imports helpers from this one. By the time a session is
		# constructed, this module is fully loaded and the dependency path is already expanded.
		from computer_use_dialogs import ComputerUseDialog
		self._dialog = ComputerUseDialog(self, hwnd, parent=parent)

	def show_dialog(self):
		"""Show the dialog so the user can type the first instruction."""
		self._dialog.bring_to_front(focus_input=True)

	def _surface_dialog(self, focus_input=False):
		"""Bring the dialog up and record that it now owns the foreground."""
		self._dialog.bring_to_front(focus_input=focus_input)
		self._dialog_visible = True

	def _hand_off_to_target(self):
		"""If the dialog is up, hide it, give the foreground to the current target window, and let
		focus settle before the next screenshot. Does nothing if the dialog is already hidden."""
		if self._dialog_visible:
			self._dialog.yield_to_target(self._target_hwnd)
			self._dialog_visible = False
			time.sleep(0.2)

	def begin(self, task):
		"""Called by the dialog, on the main thread, once the user has consented. Hand the
		foreground to the target window (so the first screenshot and actions land there, not
		on our dialog), beep that control has started, then start the control loop."""
		_set_active_session(self)
		if not self._dialog.IsBeingDeleted():
			self._dialog.Hide()
		winUser.setForegroundWindow(self._hwnd)
		self._dialog_visible = False
		on_control_start()
		self._thread = threading.Thread(target=self._run, args=(task,), daemon=True)
		self._thread.start()

	def inject_message(self, text):
		"""Queue a user message to be added before the next API call.

		Sending always hands control back to the model (answering a question it asked,
		or resuming a session the user paused), so beep that control has started. Sending
		while paused also resumes the session, so the user can pause, type a follow-up,
		and continue in one motion. Queue first, then clear, so the message is waiting
		when the paused loop wakes and drains it. Outside a pause the event isn't set, so
		clearing is a harmless no-op."""
		self._inject_queue.put(text)
		self._pause_event.clear()
		on_control_start()

	def toggle_pause(self):
		"""Flip pause state and beep accordingly. Spoken feedback is expected to be handled by the caller, depending on the reason that the session was paused."""
		if self._pause_event.is_set():
			self._pause_event.clear()
			on_control_start()
		else:
			self._pause_event.set()
			on_control_pause()

	def cancel(self):
		self._cancel_event.set()

	@property
	def is_paused(self):
		return self._pause_event.is_set()

	def _run(self, task):
		try:
			self._run_loop(task)
		finally:
			self._surface_dialog()
			self._dialog.session_ended()
			_clear_active_session(self)

	def _is_own_window(self, hwnd):
		"""True if hwnd is our computer-use dialog. The risky-action approval dialog blocks the
		worker thread on its result event rather than during a capture, so it never needs guarding
		here."""
		try:
			if not self._dialog.IsBeingDeleted() and hwnd == self._dialog.GetHandle():
				return True
		except Exception:
			log.debug("computer use: own-window check failed", exc_info=True)
		return False

	def _resolve_capture_target(self):
		"""Pick the window to screenshot this frame: the live foreground window, unless it is not a
		real window or is one of our own dialogs, in which case fall back to the last good target.
		The foreground comes from the OS (winUser), not NVDA's cached foreground object, which lags
		behind focus changes and can briefly point at a just-closed window (e.g. the consent dialog
		right after the session starts), yielding a dead handle. Returns (hwnd, obj), where obj is
		the matching NVDA foreground object for metadata, or None."""
		try:
			hwnd = winUser.getForegroundWindow()
		except Exception:
			log.debug("computer use: getForegroundWindow failed; falling back to last target", exc_info=True)
			hwnd = 0
		if not hwnd or not winUser.isWindow(hwnd) or self._is_own_window(hwnd):
			return self._target_hwnd, None
		self._target_hwnd = hwnd
		obj = None
		try:
			fg = api.getForegroundObject()
			if fg is not None and int(getattr(fg, "windowHandle", 0) or 0) == hwnd:
				obj = fg
			else:
				log.debug("computer use: foreground object does not match foreground window; no metadata")
		except Exception:
			log.debug("computer use: getForegroundObject failed; capturing without metadata", exc_info=True)
		return hwnd, obj

	def _run_loop(self, task):
		capture = Capture(self._resolve_capture_target, self._max_long_edge, self._max_pixels)
		runner = ActionRunner(self._cancel_event, self._pause_event)
		provider_session = self._service.create_computer_session(task)
		tool_results = None
		injected_text = None
		while not self._cancel_event.is_set():
			try:
				b64, cap_w, cap_h, focus = capture.capture()
			except Exception as e:
				log.error("computer use: screenshot failed", exc_info=True)
				self._dialog.append_message(f"Screenshot failed: {e}", role="system")
				break
			# Run the request on a worker thread so a pause or cancel interrupts the
			# wait instead of blocking on a slow turn until the socket times out.
			# step() does not mutate saved state, so an abandoned turn leaves the
			# provider session untouched and the retry is clean.
			status, payload = self._make_request_interruptible(
				provider_session=provider_session,
				screenshot_b64=b64,
				capture_w=cap_w,
				capture_h=cap_h,
				tool_results=tool_results,
				injected_text=injected_text,
				focus=focus,
			)
			if status == "cancelled":
				break
			if status == "paused":
				# The user paused while we waited. Abandon this turn, let them read the
				# log or type a follow-up, then loop back and re-issue the request with
				# whatever they added. Committed state is untouched, so the retry is clean.
				if not self._wait_while_paused():
					break
				followup = self._drain_injection()
				if followup:
					injected_text = " ".join(t for t in (injected_text, followup) if t)
				continue
			if status == "error":
				log.error("computer use: API request failed", exc_info=payload)
				self._dialog.append_message(f"API error: {payload}", role="system")
				tones.beep(150, 200)
				break
			resp = payload
			# Commit this turn's state before executing any actions.
			provider_session.save(resp)
			injected_text = None
			if resp.text:
				self._dialog.append_message(resp.text, role="assistant")
			if resp.is_complete or not resp.actions:
				# The model yielded its turn: either the task is done or it needs
				# something from the user. The API gives no way to tell those apart,
				# so keep the session alive and wait for a follow-up. Typing continues
				# with full context (history and response id intact); closing the
				# dialog or cancelling ends the session.
				self._dialog.append_message("Ready for your next instruction.", role="system")
				on_control_pause()
				self._surface_dialog(focus_input=True)
				followup = self._await_followup()
				if followup is None:
					break
				injected_text = followup
				tool_results = None
				# Don't hand control back yet. The model may just ask another question
				# about this input rather than act; the dialog stays up until it
				# actually issues actions (handled just before the action loop below).
				continue
			tool_results = self._execute_actions(resp, capture, runner)
			if self._cancel_event.is_set():
				break
			injected_text = self._handle_pause()

	def _execute_actions(self, resp, capture, runner):
		"""Hand control to the target window, run the model's action batch (asking approval
		for confirm/flagged actions), and return the tool_results grouped by call_id for the
		next request. Stops early if the session is cancelled or paused."""
		# The model is taking control. If our dialog is still up (we were waiting on the
		# user), hide it and hand the foreground to the target first, so input lands on the
		# target window and not on the computer control dialog.
		self._hand_off_to_target()
		# Group results by call_id: OpenAI groups multiple actions under one computer_call
		# item and expects one computer_call_output per call_id.
		results_by_call_id = {}
		for action in resp.actions:
			if self._cancel_event.is_set() or self._pause_event.is_set():
				break
			if not self._approve_all and (action.get("type") == "confirm" or action.get("safety_checks")):
				if not self._ask_approval(action):
					self._cancel_event.set()
					break
			scaled = dict(action)
			if "x" in scaled and "y" in scaled:
				scaled["x"], scaled["y"] = capture.to_screen(action["x"], action["y"])
			if "startX" in scaled:
				scaled["startX"], scaled["startY"] = capture.to_screen(action["startX"], action["startY"])
				scaled["endX"], scaled["endY"] = capture.to_screen(action["endX"], action["endY"])
			compact = runner.execute(scaled)
			self._dialog.append_message(compact, role="action")
			call_id = action.get("call_id", "")
			entry = results_by_call_id.setdefault(call_id, {"results": [], "safety_checks": action.get("safety_checks", [])})
			entry["results"].append(compact)
		return [
			{"call_id": cid, "compact_result": "\n".join(entry["results"]), "safety_checks": entry["safety_checks"]}
			for cid, entry in results_by_call_id.items()
		]

	def _handle_pause(self):
		"""Between action batches, let keystrokes settle then block while paused. Returns the
		next injected_text (a drained follow-up, or None). If the session is cancelled during
		the wait, returns None and the loop's while-condition ends the session."""
		# Let keystrokes and focus changes settle before the next screenshot
		time.sleep(0.3)
		# Pause is checked between action batches only, never mid-action.
		if not self._wait_while_paused():
			return None
		return self._drain_injection()

	def _make_request_interruptible(self, provider_session, **kwargs):
		"""Make the API request on a worker thread, polling for pause/cancel so a slow
		turn never blocks the loop until the socket times out. Returns one of:
		("ok", StepResult), ("paused", None), ("cancelled", None), ("error", exception).
		A paused or cancelled request is abandoned; its worker thread finishes (and
		fails quietly) in the background."""
		holder = {}
		done = threading.Event()
		def _worker():
			try:
				holder["resp"] = provider_session.step(**kwargs)
			except Exception as e:
				holder["error"] = e
			finally:
				done.set()
		threading.Thread(target=_worker, daemon=True).start()
		while not done.wait(0.05):
			if self._cancel_event.is_set():
				return "cancelled", None
			if self._pause_event.is_set():
				return "paused", None
		if "error" in holder:
			return "error", holder["error"]
		return "ok", holder["resp"]

	def _wait_while_paused(self):
		"""If paused, surface the dialog so the user can read the log or inject a
		follow-up, block until they resume or cancel, then hand the target window back.
		Returns False if the session was cancelled, True otherwise."""
		if not self._pause_event.is_set():
			return not self._cancel_event.is_set()
		self._surface_dialog(focus_input=True)
		while self._pause_event.is_set() and not self._cancel_event.is_set():
			time.sleep(0.05)
		if self._cancel_event.is_set():
			return False
		self._hand_off_to_target()
		return True

	def _drain_injection(self):
		"""Pull every queued follow-up message, joined into one string, or None."""
		injected = []
		while not self._inject_queue.empty():
			try:
				injected.append(self._inject_queue.get_nowait())
			except queue.Empty:
				break
		return " ".join(injected) if injected else None

	def _await_followup(self):
		"""Block until the user sends a follow-up message or ends the session.

		Returns the message text to continue with, or None if the session was
		cancelled (dialog closed or cancel gesture)."""
		while not self._cancel_event.is_set():
			try:
				return self._inject_queue.get(timeout=0.1)
			except queue.Empty:
				continue
		return None

	def _ask_approval(self, action):
		if self._request_approval is None:
			return True
		result_event = threading.Event()
		result_holder = [None]
		wx.CallAfter(self._request_approval, action, result_event, result_holder, self._target_hwnd)
		result_event.wait()
		choice = result_holder[0]
		if choice == "approve_all":
			self._approve_all = True
		return choice in ("approve_once", "approve_all")

import base64
import math
import queue
import threading
import time
from io import BytesIO

try:
	import winUser
	import screenBitmap
except ImportError:
	winUser = None
	screenBitmap = None

try:
	import ui
	import synthDriverHandler
except ImportError:
	ui = None
	synthDriverHandler = None

try:
	import tones
	import wx
except ImportError:
	tones = None
	wx = None

import dependency_checker
dependency_checker.expand_path()
from PIL import Image


ANNOUNCE_TIMEOUT_SECONDS = 10


def _announce_and_wait(text):
	if ui is None or synthDriverHandler is None:
		return
	done = threading.Event()
	def _on_done(**kwargs):
		done.set()
	# HandlerRegistrar stores only a weak reference; _on_done must stay alive
	# for the duration of this call. The stack frame keeps it alive while we block.
	synthDriverHandler.synthDoneSpeaking.register(_on_done)
	try:
		ui.message(text)
		# synthDoneSpeaking fires for any speech, not specifically this utterance.
		# Concurrent NVDA events can cause this to unblock early, which is acceptable.
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


class Capture:
	"""Captures the foreground window as a scaled base64 PNG."""

	def __init__(self, hwnd, max_long_edge=None, max_pixels=None):
		self._hwnd = hwnd
		self._max_long_edge = max_long_edge
		self._max_pixels = max_pixels
		self._scale = 1.0
		self._win_x = 0
		self._win_y = 0

	def capture(self):
		"""Returns (b64_png_str, api_w, api_h)."""
		rect = winUser.getClientRect(self._hwnd)
		cap_w = rect.right - rect.left
		cap_h = rect.bottom - rect.top
		self._win_x, self._win_y = winUser.ClientToScreen(self._hwnd, 0, 0)
		self._scale = _calculate_scale(cap_w, cap_h, self._max_long_edge, self._max_pixels)
		api_w = max(1, int(cap_w * self._scale))
		api_h = max(1, int(cap_h * self._scale))
		buf = screenBitmap.ScreenBitmap(api_w, api_h).captureImage(
			self._win_x, self._win_y, cap_w, cap_h
		)
		img = Image.frombuffer("RGB", (api_w, api_h), buf, "raw", "BGRX", 0, 1)
		out = BytesIO()
		img.save(out, format="PNG")
		return base64.b64encode(out.getvalue()).decode("ascii"), api_w, api_h

	def to_screen(self, rx, ry):
		"""Convert API-space coordinates to physical screen coordinates."""
		return int(rx / self._scale) + self._win_x, int(ry / self._scale) + self._win_y


RISKY_KEYWORDS = frozenset([
	"delete", "remove", "format", "uninstall", "password", "payment",
	"send", "submit", "purchase", "confirm", "agree", "sign in", "login",
])


def is_risky(action):
	"""True if action type is 'confirm' or any field value contains a risky keyword."""
	if action.get("type") == "confirm":
		return True
	text = " ".join(str(v) for v in action.values()).lower()
	return any(kw in text for kw in RISKY_KEYWORDS)


class ActionRunner:
	"""Executes model-issued actions using NVDA's winUser module."""

	_VK_MAP = {
		"enter": 0x0D, "return": 0x0D, "tab": 0x09, "escape": 0x1B, "esc": 0x1B,
		"space": 0x20, "backspace": 0x08, "delete": 0x2E,
		"up": 0x26, "down": 0x28, "left": 0x25, "right": 0x27,
		"home": 0x24, "end": 0x23, "pageup": 0x21, "pagedown": 0x22,
		"f1": 0x70, "f2": 0x71, "f3": 0x72, "f4": 0x73,
		"f5": 0x74, "f6": 0x75, "f7": 0x76, "f8": 0x77,
		"f9": 0x78, "f10": 0x79, "f11": 0x7A, "f12": 0x7B,
	}
	_MOD_MAP = {"ctrl": 0x11, "control": 0x11, "shift": 0x10, "alt": 0x12, "win": 0x5B}

	def execute(self, action):
		"""Execute one action dict; return a compact result string."""
		t = action.get("type", "")
		try:
			if t == "move":
				self._move(action["x"], action["y"])
				return f"move | ({action['x']}, {action['y']}) | ok"
			elif t == "left_click":
				self._click(action["x"], action["y"], "left")
				return f"left_click | ({action['x']}, {action['y']}) | ok"
			elif t == "right_click":
				self._click(action["x"], action["y"], "right")
				return f"right_click | ({action['x']}, {action['y']}) | ok"
			elif t == "middle_click":
				self._click(action["x"], action["y"], "middle")
				return f"middle_click | ({action['x']}, {action['y']}) | ok"
			elif t == "double_click":
				self._click(action["x"], action["y"], "left")
				time.sleep(0.05)
				self._click(action["x"], action["y"], "left")
				return f"double_click | ({action['x']}, {action['y']}) | ok"
			elif t == "triple_click":
				for _ in range(3):
					self._click(action["x"], action["y"], "left")
					time.sleep(0.05)
				return f"triple_click | ({action['x']}, {action['y']}) | ok"
			elif t == "left_click_drag":
				self._drag(action["startX"], action["startY"], action["endX"], action["endY"])
				return f"left_click_drag | ({action['startX']},{action['startY']})->({action['endX']},{action['endY']}) | ok"
			elif t == "scroll":
				self._scroll(action["x"], action["y"], action.get("direction", "down"), action.get("amount", 3))
				return f"scroll | ({action['x']}, {action['y']}) {action.get('direction', 'down')} {action.get('amount', 3)} | ok"
			elif t == "key":
				self._key(action["key"])
				return f"key | {action['key']} | ok"
			elif t == "type":
				preview = action["text"][:40]
				_announce_and_wait(f"Typing {preview}")
				self._type_text(action["text"])
				return f"type | {preview} | ok"
			elif t == "wait":
				time.sleep(0.5)
				return "wait | 500ms | ok"
			elif t == "screenshot":
				_announce_and_wait("Taking screenshot...")
				return "screenshot | (handled by loop) | ok"
			else:
				return f"{t} | (unknown) | skipped"
		except Exception as e:
			return f"{t} | error | {e}"

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
		main_key = parts[-1].strip()
		modifiers = [self._MOD_MAP[p.strip()] for p in parts[:-1] if p.strip() in self._MOD_MAP]
		for vk in modifiers:
			winUser.keybd_event(vk, 0, 0, 0)
		main_vk = self._VK_MAP.get(main_key)
		extra_shift = False
		if main_vk is None and main_key:
			try:
				shift_state, main_vk = winUser.VkKeyScanEx(main_key[0], 0)
				if shift_state & 0x01 and 0x10 not in modifiers:
					extra_shift = True
					winUser.keybd_event(0x10, 0, 0, 0)
			except LookupError:
				pass
		if main_vk is not None:
			winUser.keybd_event(main_vk, 0, 0, 0)
			winUser.keybd_event(main_vk, 0, winUser.KEYEVENTF_KEYUP, 0)
		if extra_shift:
			winUser.keybd_event(0x10, 0, winUser.KEYEVENTF_KEYUP, 0)
		for vk in reversed(modifiers):
			winUser.keybd_event(vk, 0, winUser.KEYEVENTF_KEYUP, 0)

	def _type_text(self, text):
		try:
			for ch in text:
				if ch == "\n":
					winUser.keybd_event(0x0D, 0, 0, 0)
					winUser.keybd_event(0x0D, 0, winUser.KEYEVENTF_KEYUP, 0)
				else:
					cp = ord(ch)
					winUser.keybd_event(0, cp, winUser.KEYEVENTF_UNICODE, 0)
					winUser.keybd_event(0, cp, winUser.KEYEVENTF_UNICODE | winUser.KEYEVENTF_KEYUP, 0)
		except Exception:
			try:
				with winUser.openClipboard():
					winUser.setClipboardData(winUser.CF_UNICODETEXT, text)
				winUser.keybd_event(0x11, 0, 0, 0)  # Ctrl down
				winUser.keybd_event(0x56, 0, 0, 0)  # V down
				winUser.keybd_event(0x56, 0, winUser.KEYEVENTF_KEYUP, 0)
				winUser.keybd_event(0x11, 0, winUser.KEYEVENTF_KEYUP, 0)
			except Exception:
				pass


class ComputerUseSession:
	"""Orchestrates the agentic control loop on a background thread."""

	def __init__(self, service, hwnd, on_message, cancel_event, pause_event, request_approval=None, dialog=None):
		self._service = service
		self._hwnd = hwnd
		self._on_message = on_message
		self._cancel_event = cancel_event
		self._pause_event = pause_event
		self._request_approval = request_approval
		self._dialog = dialog
		self._inject_queue = queue.Queue()
		self._approve_all = False
		self._thread = None
		self._max_long_edge = getattr(service, "_capture_max_long_edge", None)
		self._max_pixels = getattr(service, "_capture_max_pixels", None)

	def start(self, task):
		self._thread = threading.Thread(target=self._run, args=(task,), daemon=True)
		self._thread.start()

	def inject_message(self, text):
		"""Queue a user message to be added before the next API call."""
		self._inject_queue.put(text)

	def _run(self, task):
		capture = Capture(self._hwnd, self._max_long_edge, self._max_pixels)
		runner = ActionRunner()
		history = []
		previous_response_id = None
		tool_results = None
		injected_text = None

		while not self._cancel_event.is_set():
			try:
				b64, cap_w, cap_h = capture.capture()
			except Exception as e:
				self._on_message(f"Screenshot failed: {e}", role="system")
				break

			try:
				resp = self._service.make_computer_use_request(
					screenshot_b64=b64,
					capture_w=cap_w,
					capture_h=cap_h,
					task=task,
					history=history,
					previous_response_id=previous_response_id,
					tool_results=tool_results,
					injected_text=injected_text,
				)
			except Exception as e:
				self._on_message(f"API error: {e}", role="system")
				previous_response_id = None
				break

			injected_text = None

			if resp.get("text"):
				self._on_message(resp["text"], role="assistant")

			if resp.get("is_complete") or not resp.get("actions"):
				self._on_message("Task complete.", role="system")
				if tones:
					tones.beep(108, 300)
				if wx and self._dialog:
					wx.CallAfter(self._dialog.SetFocus)
				break

			previous_response_id = resp.get("response_id")
			# Group results by call_id: OpenAI groups multiple actions under one
			# computer_call item and expects one computer_call_output per call_id.
			results_by_call_id = {}
			for action in resp["actions"]:
				if self._cancel_event.is_set():
					break
				if not self._approve_all and (action.get("type") == "confirm" or is_risky(action)):
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
				self._on_message(compact, role="action")
				call_id = action.get("_call_id", "")
				results_by_call_id.setdefault(call_id, []).append(compact)
			tool_results = [
				{"call_id": cid, "compact_result": "\n".join(results)}
				for cid, results in results_by_call_id.items()
			]
			if self._cancel_event.is_set():
				break
			# Let keystrokes and focus changes settle before the next screenshot
			time.sleep(0.3)
			# Pause is checked between action batches only, never mid-action
			while self._pause_event.is_set() and not self._cancel_event.is_set():
				time.sleep(0.05)
			injected = []
			while not self._inject_queue.empty():
				injected.append(self._inject_queue.get_nowait())
			if injected:
				injected_text = " ".join(injected)

	def _ask_approval(self, action):
		if self._request_approval is None:
			return True
		result_event = threading.Event()
		result_holder = [None]
		import wx
		wx.CallAfter(self._request_approval, action, result_event, result_holder)
		result_event.wait()
		choice = result_holder[0]
		if choice == "approve_all":
			self._approve_all = True
		return choice in ("approve_once", "approve_all")

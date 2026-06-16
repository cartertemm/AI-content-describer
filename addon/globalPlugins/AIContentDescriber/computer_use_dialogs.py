import wx

import logging
log = logging.getLogger(__name__)

import ui
import addonHandler
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Couldn't initialise translations for the computer use dialog.")

import gui
import winUser
from computer_use import _announce_and_wait, yield_foreground_to, _on_main_thread, describe_action, safety_check_messages


def _get_pause_gesture():
	try:
		import globalPluginHandler
		import inputCore
		for plugin in globalPluginHandler.runningPlugins:
			if not hasattr(plugin, 'script_pause_resume_computer_use'):
				continue
			for identifier, func in plugin._gestureMap.items():
				if getattr(func, '__name__', '') == 'script_pause_resume_computer_use':
					return inputCore.getDisplayTextForGestureIdentifier(identifier)[1]
	except Exception:
		log.exception("Couldn't resolve the pause/resume gesture; falling back to the default.")
	return "NVDA+Control+Shift+P"


class ComputerUseDialog(wx.Dialog):
	"""Dialog for an AI computer-control session: a read-only log plus an input box.

	The session owns this dialog and calls append_message / bring_to_front /
	yield_to_target / session_ended on it. The dialog raises the consent prompt on the
	first message and forwards later messages to the session."""

	def __init__(self, session, hwnd, parent=None):
		# Translators: Title for the computer control session dialog
		super().__init__(parent=parent, title=_("Computer Control Session"))
		self._session = session
		self._hwnd = hwnd
		self._session_started = False
		self._init_ui()
		self.Centre()
		self.Bind(wx.EVT_CLOSE, self.on_close)

	def _init_ui(self):
		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		# Translators: label of the read-only history field in the computer control dialog
		history_label = wx.StaticText(panel, label=_("&History:"))
		vbox.Add(history_label, flag=wx.LEFT | wx.TOP, border=15)
		self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
		vbox.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=15)
		# Translators: label of the message field in the computer control dialog
		message_label = wx.StaticText(panel, label=_("Enter Your Message:"))
		vbox.Add(message_label, flag=wx.LEFT, border=15)
		self.input_txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
		self.input_txt.Bind(wx.EVT_TEXT_ENTER, self.on_send)
		vbox.Add(self.input_txt, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: the Send button in the computer control dialog
		self.send_button = wx.Button(panel, label=_("&Send"))
		self.send_button.Bind(wx.EVT_BUTTON, self.on_send)
		hbox.Add(self.send_button, flag=wx.RIGHT, border=8)
		# Translators: the Save Output button in the computer control dialog
		self.save_button = wx.Button(panel, label=_("Save &Output"))
		self.save_button.Bind(wx.EVT_BUTTON, self.on_save_output)
		hbox.Add(self.save_button, flag=wx.RIGHT, border=8)
		# Translators: the Close button in the computer control dialog
		self.close_button = wx.Button(panel, label=_("Close"))
		self.SetEscapeId(self.close_button.GetId())
		self.close_button.Bind(wx.EVT_BUTTON, self.on_close)
		hbox.Add(self.close_button)
		vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)
		panel.SetSizer(vbox)
		self.SetSize((750, 500))
		self.SetMinSize((600, 400))
		self.input_txt.SetFocus()

	def append_message(self, text, role="system"):
		"""Append a role-prefixed line to the log. Speak only the model's own messages,
		using announce-and-wait so they are not cut off by the next action announcement."""
		prefixes = {
			"action": "[action] ",
			"assistant": _("AI: "),
			"system": "[system] ",
			"user": _("You: "),
		}
		prefix = prefixes.get(role, f"{role}: ")
		_on_main_thread(lambda: self.text_ctrl.AppendText(f"{prefix}{text}\n"))
		if role == "assistant":
			_announce_and_wait(text)

	def bring_to_front(self, focus_input=False):
		"""Brings this dialog to the foreground, optionally focusing the text field."""
		def _do():
			if self.IsBeingDeleted():
				return
			self.Show()
			self.Raise()
			if focus_input:
				self.input_txt.SetFocus()
			else:
				self.SetFocus()
		_on_main_thread(_do)

	def yield_to_target(self, hwnd=None):
		"""Hide this dialog and hand the foreground to the target window. `hwnd` lets the session
		pass the live target; falls back to the window the dialog was opened for."""
		target = hwnd if hwnd is not None else self._hwnd
		def _do():
			if not self.IsBeingDeleted():
				self.Hide()
			yield_foreground_to(target)
		_on_main_thread(_do)

	def session_ended(self):
		"""Called when the session loop has finished. A clean end has no beep, so log and
		speak that it ended, then stop forwarding input to a dead session."""
		# Translators: logged and spoken when a computer control session ends
		message = _("Session ended")
		self.append_message(message, role="system")
		ui.message(message)
		def _do():
			if not self.IsBeingDeleted():
				self.input_txt.Disable()
				self.send_button.Disable()
		_on_main_thread(_do)

	def on_send(self, event=None):
		text = self.input_txt.GetValue().strip()
		if not text:
			self.input_txt.SetFocus()
			return
		self.input_txt.SetValue("")
		if not self._session_started:
			self._request_consent(text)
		else:
			self.append_message(text, role="user")
			self._session.inject_message(text)
		self.input_txt.SetFocus()

	def _request_consent(self, task):
		keystroke = _get_pause_gesture()
		dlg = wx.MessageDialog(
			self,
			# Translators: body of the computer control consent dialog
			_("The selected model would like to take control of your computer to perform the requested task. You will be notified as actions occur, and you can press {keystroke} any time to pause the session. Would you like to allow this?").format(keystroke=keystroke),
			# Translators: title of the computer control consent dialog
			_("AI Content Describer"),
			wx.YES_NO | wx.ICON_QUESTION,
		)
		winUser.setForegroundWindow(dlg.GetHandle())
		# Translators: spoken when the consent dialog appears, to alert the user to switch to it
		ui.message(_("Consent required. Please check the dialog."))
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_YES:
			self.append_message(task, role="user")
			self._session_started = True
			self._session.begin(task)
		else:
			# Translators: shown in session history when the user declines consent
			self.append_message(_("Session declined by user"), role="system")

	def on_save_output(self, event):
		with wx.FileDialog(
			self,
			# Translators: prompt in the save file dialog
			_("Save conversation"),
			wildcard=_("Text files (*.txt)|*.txt"),
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
		) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			try:
				with open(fileDialog.GetPath(), "w", encoding="utf-8") as f:
					f.write(self.text_ctrl.GetValue())
				# Translators: spoken when the session log is saved
				ui.message(_("Conversation saved"))
			except IOError:
				ui.message(_("Error saving file"))

	def on_close(self, event):
		self._session.cancel()
		self.Destroy()


class ComputerUseApprovalDialog(wx.Dialog):
	"""Asks the user to approve a risky or confirm-type action before it executes."""

	def __init__(self, parent, action):
		# Translators: title of the dialog asking whether to allow a risky AI action
		super().__init__(parent, title=_("Approve Action"))
		self.choice = "cancel"
		sizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: body of the risky-action approval dialog; {action} is a description of what the AI wants to do
		body = _("The AI wants to perform a potentially risky action:\n\n{action}\n\nAllow it?").format(action=describe_action(action))
		messages = safety_check_messages(action)
		if messages:
			# Translators: header for API-issued safety warnings appended to the approval dialog
			body += "\n\n" + _("API safety warnings:") + "\n" + "\n".join(f"- {m}" for m in messages)
		msg = wx.StaticText(self, label=body)
		sizer.Add(msg, 0, wx.ALL, 10)
		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: button to deny the AI action and stop the session
		cancel_btn = wx.Button(self, label=_("&Cancel"))
		# Translators: button to allow this one AI action
		once_btn = wx.Button(self, label=_("Approve &Once"))
		# Translators: button to allow all remaining AI actions without further prompting
		all_btn = wx.Button(self, label=_("Approve &All"))
		btn_sizer.Add(cancel_btn, flag=wx.RIGHT, border=8)
		btn_sizer.Add(once_btn, flag=wx.RIGHT, border=8)
		btn_sizer.Add(all_btn)
		sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)
		self.SetSizer(sizer)
		self.Fit()
		cancel_btn.SetFocus()
		cancel_btn.Bind(wx.EVT_BUTTON, lambda e: self._close("cancel"))
		once_btn.Bind(wx.EVT_BUTTON, lambda e: self._close("approve_once"))
		all_btn.Bind(wx.EVT_BUTTON, lambda e: self._close("approve_all"))
		# Closing via the window's X button must also release the session thread
		self.Bind(wx.EVT_CLOSE, lambda e: self._close("cancel"))

	def _close(self, choice):
		self.choice = choice
		self.EndModal(wx.ID_OK)


def show_computer_use_approval(action, result_event, result_holder, target_hwnd=None):
	"""Called on the main thread by ComputerUseSession for risky actions."""
	dlg = ComputerUseApprovalDialog(gui.mainFrame, action)
	dlg.ShowModal()
	result_holder[0] = dlg.choice
	dlg.Destroy()
	# Restore the target window's foreground while we still own it so the
	# approved action's input goes to the user's app.
	# Otherwise, actions will be sent to the computer use dialog
	if target_hwnd and result_holder[0] in ("approve_once", "approve_all"):
		yield_foreground_to(target_hwnd)
	result_event.set()

import threading
import wx
import os

import ui
import logging
log = logging.getLogger(__name__)
import addonHandler
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	pass

# Global variable to hold dialog reference
_conversation_dialog = None

class MultimodalInput(wx.Dialog):
	def __init__(self, service, parent=None, title=None, *args, **kwargs):
		self.service = service
		if title is None:
			# Translators: Default title for the multimodal conversation dialog
			title = _("AI Conversation - {model}").format(model=service.name)
		super().__init__(parent=parent, title=title, *args, **kwargs)
		self.current_image_path = None
		self.files = []  # the files (images) that are a part of the conversation and need to be cleaned up when this dialog is destroyed
		self.include_original_image = True
		self.init_ui()
		self.load_conversation_history()
		self.Centre()
		# Clean up when dialog closes
		self.Bind(wx.EVT_CLOSE, self.on_close)

	def init_ui(self):
		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		# translators: The label of the read-only image field in the conversation dialog.
		image_label = wx.StaticText(panel, label=_("Image:"))
		vbox.Add(image_label, flag=wx.LEFT | wx.TOP, border=15)
		image_hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.image_field = wx.TextCtrl(panel, style=wx.TE_READONLY)
		# hack: Read-only input elements do not get focus from the tab key by default
		# so we have to patch this function.
		self.image_field.AcceptsFocusFromKeyboard = lambda:True
		image_hbox.Add(self.image_field, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=8)
		# translators: The label of the Browse button in the conversation dialog.
		self.browse_button = wx.Button(panel, label=_("&Browse"))
		self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse_image)
		image_hbox.Add(self.browse_button, flag=wx.RIGHT, border=8)
		# translators: The label of the Delete button in the conversation dialog.
		self.delete_button = wx.Button(panel, label=_("&Delete"))
		self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete_image)
		image_hbox.Add(self.delete_button)
		vbox.Add(image_hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)
		# Translators: the include original image checkbox in the conversation dialog.
		self.include_original_checkbox = wx.CheckBox(panel, label=_("Include original image in context"))
		self.include_original_checkbox.SetValue(True)
		self.include_original_checkbox.Bind(wx.EVT_CHECKBOX, self.on_include_original_changed)
		vbox.Add(self.include_original_checkbox, flag=wx.LEFT | wx.TOP | wx.BOTTOM, border=15)
		# translators: The label of the read-only multi-line history field in the conversation dialog.
		history_label = wx.StaticText(panel, label=_("&History:"))
		vbox.Add(history_label, flag=wx.LEFT, border=15)
		self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
		vbox.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=15)
		# translators: The label of the message field in the conversation dialog.
		message_label = wx.StaticText(panel, label=_("Enter Your Message:"))
		vbox.Add(message_label, flag=wx.LEFT, border=15)
		self.input_txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
		self.input_txt.SetFocus()
		self.input_txt.Bind(wx.EVT_TEXT_ENTER, self.on_send)
		vbox.Add(self.input_txt, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)
		# Buttons
		hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
		# translators: The label of the options button in the conversation dialog.
		self.options_button = wx.Button(panel, label=_("&Options"))
		self.options_button.Bind(wx.EVT_BUTTON, self.on_options)
		hbox_buttons.Add(self.options_button, flag=wx.RIGHT, border=8)
		# translators: The label of the Send button in the conversation dialog.
		self.send_button = wx.Button(panel, label=_("&Send"))
		self.send_button.Bind(wx.EVT_BUTTON, self.on_send)
		hbox_buttons.Add(self.send_button, flag=wx.RIGHT, border=8)
		# Translators: The label of the Close button in the conversation dialog.
		self.close_button = wx.Button(panel, label=_("Close"))
		self.SetEscapeId(self.close_button.GetId())
		self.close_button.Bind(wx.EVT_BUTTON, self.on_close)
		hbox_buttons.Add(self.close_button)
		vbox.Add(hbox_buttons, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)
		panel.SetSizer(vbox)
		self.SetSize((750, 500))
		self.SetMinSize((600, 400))

	def load_conversation_history(self):
		"""Load conversation history from service"""
		if not self.service.has_conversation():
			return
		conversation = self.service._conversations.get(self.service._active_conversation, [])
		for message in conversation:
			role = message["role"]
			content = message["content"]
			if role == "user":
				# translators: The text placed before a message sent by you in the conversation dialog's history buffer. This is also spoken upon receipt of a new message.
				prefix = _("You: ")
				# Set image field if this is the first user message with an image
				if message.get("image") and not self.current_image_path:
					# Try to find the original image path from the conversation ID if it's an image hash
					if self.service._active_conversation and not self.service._active_conversation.startswith("text_chat"):
						# translators: Value placed in the read-only image field when the original image has been added to the chat in the conversation dialog.
						self.image_field.SetValue(_("Original image (from initial description)"))
					else:
						# translators: Value placed in the read-only image field of the conversation dialog when a new image has been attached.
						self.image_field.SetValue(_("Image attached"))
			elif role == "assistant":
				# translators: The text placed before a message from the AI in the conversation dialog's history buffer. This is also spoken upon receipt of a new message.
				prefix = _("AI: ")
			else:
				prefix = f"{role.title()}: "
			self.text_ctrl.AppendText(prefix + content + "\n")

	def on_browse_image(self, event):
		"""Handle browse button click"""
		with wx.FileDialog(
			self,
			# translators: The prompt to choose an image in the file dialog.
			_("Choose an image"),
			wildcard=_("Image files (*.jpg;*.jpeg;*.png;*.gif;*.webp)|*.jpg;*.jpeg;*.png;*.gif;*.webp"),
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			pathname = fileDialog.GetPath()
			self.current_image_path = pathname
			self.image_field.SetValue(os.path.basename(pathname))

	def on_delete_image(self, event):
		"""Handle delete button click"""
		self.current_image_path = None
		self.image_field.SetValue("")

	def on_include_original_changed(self, event):
		"""Handle include original image checkbox"""
		self.include_original_image = event.IsChecked()

	def on_send(self, event):
		"""Handle send button/enter key"""
		user_input = self.input_txt.GetValue().strip()
		if not user_input:
			self.input_txt.SetFocus()
			return
		self.input_txt.SetValue("")
		self.send_button.Enable(False)
		# Show user message immediately
		text_entry = _("You: ") + user_input + "\n"
		self.text_ctrl.AppendText(text_entry)
		ui.message(text_entry)
		# Show thinking indicator
		# translators: The message shown in the multi-line read-only history field when the AI is processing the user's input.
		self.text_ctrl.AppendText(_("AI: (thinking...)") + "\n")
		# Start API call directly (no threading as per user's modifications)
		threading.Thread(target=self.get_ai_response, args=[user_input], daemon=True).start()

	def get_ai_response(self, user_input):
		"""Get the response from the AI.
		This is run in a separate thread as to prevent blocking the main one."""
		try:
			# Use the conversation system
			if not self.service.has_conversation():
				# This shouldn't happen, but handle gracefully
				# translators: Message spoken when there is no active conversation in the conversation dialog.
				self.show_error(_("No active conversation. Please restart the dialog."))
				return
			response = self.service.add_to_conversation(
				user_input, 
				image_path=self.current_image_path,
				include_original_image=self.include_original_image
			)
			wx.CallAfter(self.on_response_received, response)
		except Exception as e:
			wx.CallAfter(self.show_error, str(e))

	def on_response_received(self, response):
		"""Handle AI response on main thread"""
		# Remove the "thinking..." line
		current_text = self.text_ctrl.GetValue()
		if current_text.endswith(_("AI: (thinking...)") + "\n"):
			lines = current_text.split('\n')
			lines = lines[:-2]  # Remove empty line and thinking line
			self.text_ctrl.SetValue('\n'.join(lines) + '\n')
		self.text_ctrl.AppendText(_("AI: ") + response + "\n")
		ui.message(response)
		self.send_button.Enable(True)
		self.input_txt.SetFocus()
		if self.current_image_path:
			self.current_image_path = None
			self.image_field.SetValue("")

	def show_error(self, error_message):
		"""Show error in the output field"""
		self.text_ctrl.AppendText(_("Error: ") + error_message + "\n")
		ui.message(_("Error: ") + error_message)
		self.send_button.Enable(True)
		self.input_txt.SetFocus()

	def on_options(self, event):
		"""Handle options button"""
		popup_menu = wx.Menu()
		# translators: The clear conversation option under options in the conversation dialog.
		clear_item = popup_menu.Append(wx.ID_ANY, _("&Clear Conversation"))
		self.Bind(wx.EVT_MENU, self.on_clear_conversation, clear_item)
		# translators: The save output to file option under options in the conversation dialog.
		save_item = popup_menu.Append(wx.ID_ANY, _("&Save Output to File"))
		self.Bind(wx.EVT_MENU, self.on_save_output, save_item)
		self.PopupMenu(popup_menu, self.options_button.GetPosition())
		popup_menu.Destroy()

	def on_clear_conversation(self, event):
		"""Clear the current conversation"""
		if self.service.has_conversation():
			self.service.clear_conversation()
		self.text_ctrl.Clear()
		# translators: Message spoken when the conversation has been cleared in the conversation dialog.
		ui.message(_("Conversation cleared"))

	def on_save_output(self, event):
		"""Save conversation to file"""
		with wx.FileDialog(
			self,
			# translators: The prompt in the save file dialog.
			_("Save conversation"),
			wildcard=_("Text files (*.txt)|*.txt"),
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
		) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			pathname = fileDialog.GetPath()
			try:
				with open(pathname, "w", encoding="utf-8") as file:
					file.write(self.text_ctrl.GetValue())
				# translators: The message spoken when a conversation has been saved to disk from the conversation dialog.
				ui.message(_("Conversation saved"))
			except IOError:
				ui.message(_("Error saving file"))

	def on_close(self, event):
		"""Handle dialog close"""
		global _conversation_dialog
		_conversation_dialog = None
		for file in self.files:
			log.debug("Cleaning up image: "+file)
			os.unlink(file)
		self.files = []
		self.Destroy()

	def attach_new_image(self, image_path, delete=True):
		"""Attach a new image to the conversation (called from main plugin)"""
		if not image_path or not os.path.exists(image_path):
			return False
		# Ask user if they want to attach to current conversation
		dlg = wx.MessageDialog(
			self,
			# translators: The body of the yes/no dialog asking the user whether they would like to attach the image they just described to the open conversation.
			_("Would you like to attach this image to the current conversation?"),
			# translators: The title of the attach image yes/no dialog.
			_("Attach Image"),
			wx.YES_NO | wx.ICON_QUESTION
		)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_YES:
			self.current_image_path = image_path
			if delete:
				self.files.append(image_path)
			self.image_field.SetValue(os.path.basename(image_path))
			self.Raise()  # Bring dialog to front
			self.input_txt.SetFocus()
			return True
		return False


def launch_conversation_dialog(service, parent=None):
	"""Launch or bring to front the conversation dialog"""
	global _conversation_dialog
	if _conversation_dialog and _conversation_dialog.IsShown() and _conversation_dialog.service == service:
		# Dialog already exists for this service, bring it to front
		_conversation_dialog.Raise()
		_conversation_dialog.input_txt.SetFocus()
		return _conversation_dialog
	# Create new dialog
	_conversation_dialog = MultimodalInput(service, parent)
	_conversation_dialog.Show()
	return _conversation_dialog


def offer_image_attachment(image_path, delete=False):
	"""
	Called from main plugin when user describes an image while dialog is open.
	Returns True if image was attached to existing conversation, False if new conversation should be created.
	"""
	global _conversation_dialog
	if _conversation_dialog and _conversation_dialog.IsShown():
		return _conversation_dialog.attach_new_image(image_path, delete=delete)
	return False

# add prompt specific timeout and caching

# *-* coding: utf-8 *-*

# NVDA Add-on: Ai Content Describer
# Copyright (C) 2023, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import sys
import os
import tempfile
import threading
import logging
log = logging.getLogger(__name__)

import api
import addonHandler

try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Couldn't initialise translations. Is this addon running from NVDA's scratchpad directory?")

import wx
import globalVars
import gui
from gui import guiHelper
from gui import nvdaControls
from gui.settingsDialogs import SettingsPanel
import tones
import ui
from globalPluginHandler import GlobalPlugin


# third party (packaged) modules
module_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(module_path)
import config_handler as ch
import description_service
import model_configuration
from multimodal_input import launch_conversation_dialog, offer_image_attachment, MultimodalInput
from computer_use import ComputerUseSession
import dependency_checker
import computer_control

third_party_path = dependency_checker.expand_path()
# stdlib additions to import markdown
import html
html.__path__.append(os.path.join(third_party_path, "html"))
import xml
xml.__path__.append(os.path.join(third_party_path, "xml"))
import markdown
from markdown.extensions import fenced_code, nl2br, tables, sane_lists
html.__path__.pop()
xml.__path__.pop()
from PIL import ImageGrab


# ugly hack: since OpenCV takes time to initialize on some machines, do it in a thread as to prevent intermittent lag elsewhere
face_view = None
cv2 = None
def threaded_imports():
	global cv2, face_view
	try:
		import cv2
		import face_view
		GlobalPlugin.detection_interface = face_view.fd
		GlobalPlugin.detection_interface_error = None
	except Exception as exc:
		GlobalPlugin.detection_interface_error = str(exc)
		raise
	finally:
		sys.path.remove(module_path)
		dependency_checker.collapse_path()
threading.Thread(target=threaded_imports).start()


service = None


def launch_models_dialog(parent):
	dialog = model_configuration.build_model_configuration_dialog(parent)
	gui.mainFrame.popupSettingsDialog(dialog)


def set_model_from_config():
	global service
	last_used = ch.config["global"]["last_used_model"]
	if last_used:
		service = description_service.get_model_by_name(last_used)


class AIDescriberSettingsPanel(SettingsPanel):
	# Translators: The label for the category in NVDA settings
	title = _("AI Content Describer")

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# translators: the button in the settings dialog to open the model manager
		self.models_dialog_button = sHelper.addItem(wx.Button(self, label=_("Manage &models")))
		# translators: the label for the dropdown that lists the currently available models
		self.available_models = sHelper.addLabeledControl(_("Model (configure more in the manage models dialog, defaults to last used):"), wx.Choice)
		# Translators: The label for the option to open results in browsable dialogs
		self.open_in_dialog = sHelper.addItem(wx.CheckBox(self, label=_("Open each result in a browsable dialog; Markdown will be rendered if possible")))
		# Translators: The label for the checkbox to cash images and their descriptions in the settings dialog
		self.cache_descriptions = sHelper.addItem(wx.CheckBox(self, label=_("Remember/cache descriptions of each item to save API quota")))
		# Translators: The label for the checkbox that controls whether to optimize image uploads for size in the settings dialog
		self.optimize_for_size = sHelper.addItem(wx.CheckBox(self, label=_("Optimize images for size, may speed up detection in some situations (experimental)")))
		self.bind_events()
		self.populate_values()

	def bind_events(self):
		self.Bind(wx.EVT_BUTTON, self.on_models_dialog, self.models_dialog_button)

	def populate_values(self):
		available = description_service.list_available_model_names()
		if len(available) > 0:
			self.available_models.Clear()
			self.available_models.Set(available)
			last_used = ch.config["global"]["last_used_model"]
			if last_used in available:
				self.available_models.SetSelection(available.index(last_used))
			else:  # it became unavailable for some reason, so just go with the first
				self.available_models.SetSelection(0)
		else:
			self.available_models.Clear()
		if service is not None:
			self.cache_descriptions.SetValue(ch.config[service.name]["cache_descriptions"])
		self.open_in_dialog.SetValue(ch.config["global"]["open_in_dialog"])
		self.optimize_for_size.SetValue(ch.config["global"]["optimize_for_size"])

	def on_models_dialog(self, event):
		launch_models_dialog(self)

	def onSave(self):
		available = description_service.list_available_model_names()
		selection = self.available_models.GetSelection()
		if len(available) > 0:
			if len(available) > selection:
				ch.config["global"]["last_used_model"] = available[selection]
				set_model_from_config()
		if service is not None:
			ch.config[service.name]["cache_descriptions"] = self.cache_descriptions.GetValue()
		ch.config["global"]["optimize_for_size"] = self.optimize_for_size.GetValue()
		ch.config["global"]["open_in_dialog"] = self.open_in_dialog.GetValue()
		ch.config.write()



class ComputerUseApprovalDialog(wx.Dialog):
	"""Asks the user to approve a risky or confirm-type action before it executes."""

	def __init__(self, parent, action):
		action_type = action.get("type", "unknown")
		action_desc = action_type
		if "x" in action and "y" in action:
			action_desc += f" at ({action['x']}, {action['y']})"
		if "text" in action:
			action_desc += f": {action['text'][:60]}"
		if "key" in action:
			action_desc += f": {action['key']}"
		# Translators: title of the dialog asking whether to allow a risky AI action
		super().__init__(parent, title=_("Approve Action"))
		self.choice = "cancel"
		sizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: body of the risky-action approval dialog; {action} is a description of what the AI wants to do
		body = _("The AI wants to perform a potentially risky action:\n\n{action}\n\nAllow it?").format(action=action_desc)
		safety_checks = action.get("_safety_checks", [])
		if safety_checks:
			messages = [sc.get("message") or sc.get("code", "") for sc in safety_checks]
			messages = [m for m in messages if m]
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


def _show_computer_use_approval(action, result_event, result_holder, target_hwnd=None):
	"""Called on main thread by ComputerUseSession for risky actions."""
	dlg = ComputerUseApprovalDialog(gui.mainFrame, action)
	dlg.ShowModal()
	result_holder[0] = dlg.choice
	dlg.Destroy()
	# Restore the target window's foreground while we still own it so the
	# approved action's input goes to the user's app, not elsewhere.
	if target_hwnd and result_holder[0] in ("approve_once", "approve_all"):
		import winUser
		winUser.setForegroundWindow(target_hwnd)
	result_event.set()


class AreaMenu(wx.Menu):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.selection = None
		# translators: current focus
		self.focus_item = self.Append(wx.ID_ANY, _("Current focus"))
		# translators: navigator object
		self.navigator_item = self.Append(wx.ID_ANY, _("Navigator object"))
		# translators: screenshot of entire window menu item
		self.screenshot_item = self.Append(wx.ID_ANY, _("Entire screen"))
		# translators: menu item to reconstruct the screen as accessible HTML
		self.show_ui_item = self.Append(wx.ID_ANY, _("Show UI"))
		# translators: picture from the local camera menu item
		self.camera_item = self.Append(wx.ID_ANY, _("Take a picture"))
		# For the face detection submenu
		self.face_detection_menu = wx.Menu()
		self.detect_face_item = self.face_detection_menu.Append(wx.ID_ANY, _("Detect face position"))
		#self.detect_face_realtime_item = self.face_detection_menu.Append(wx.ID_ANY, _("Real-time face guidance"))
		self.select_camera_item = self.face_detection_menu.Append(wx.ID_ANY, _("Select camera"))
		self.release_camera_item = self.face_detection_menu.Append(wx.ID_ANY, _("Release the camera to make it usable by other applications"))
		# translators: the label for the submenu that contains the options for face detection. Also informs the user that this feature does not require API access.
		self.AppendSubMenu(self.face_detection_menu, _("Face Detection (no API required)"))
		# For the model selector
		self.model_menu = wx.Menu()
		self.available_models = description_service.list_available_model_names()
		last_used = ch.config["global"]["last_used_model"]
		for model in self.available_models:
			item = self.model_menu.AppendRadioItem(wx.ID_ANY, model)
			if model == last_used:
				item.Check()
			gui.mainFrame.Bind(wx.EVT_MENU, self.on_new_model, item)
		# translators: the name of the submenu used to select a model.
		self.AppendSubMenu(self.model_menu, _("Model"))
		if service and service.has_conversation():
			# translators: the label for the item to follow-up on the last description
			self.followup_item = self.Append(wx.ID_ANY, _("Follow-up on previous description"))
			gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.followup_item)
		else:
			self.followup_item = None
		if service and service.supports_computer_use:
			# Translators: area menu item to start an AI computer control session
			self.computer_use_item = self.Append(wx.ID_ANY, _("Control computer..."))
		else:
			# Translators: area menu item shown when the selected model does not support computer control
			self.computer_use_item = self.Append(wx.ID_ANY, _("Control computer (not supported by selected model)"))
			self.computer_use_item.Enable(False)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.computer_use_item)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.focus_item)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.navigator_item)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.screenshot_item)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.show_ui_item)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.camera_item)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.detect_face_item)
		#gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.detect_face_realtime_item)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.select_camera_item)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.release_camera_item)

	def on_menu_selected(self, event):
		self.selection = self.FindItemById(event.GetId())

	def on_new_model(self, event):
		item = self.model_menu.FindItemById(event.GetId())
		ch.config["global"]["last_used_model"] = item.GetItemLabelText()
		ch.config.write()
		set_model_from_config()


class GlobalPlugin(GlobalPlugin):
	scriptCategory = _("AI Content Describer")

	def __init__(self, *args, **kwargs):
		global service
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(AIDescriberSettingsPanel)
		ch.load_config()
		if ch.migrate_config_if_needed():
			ch.config.write()
		set_model_from_config()

		# cache the previous focus and navigator objects globally, as popping up a menu seems to alter them
		self.prev_focus = None
		self.prev_navigator = None

	def terminate(self):
		super().terminate()
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(AIDescriberSettingsPanel)

	def describe_navigator_object(self):
		return self.describe_object(focus=False)

	def describe_focus_object(self):
		return self.describe_object(focus=True)


	def describe_object(self, focus=False):
		if self.is_screen_curtain_running():
			# Translators: message spoken when there is an attempt to recognize an object, but the screen curtain is running
			ui.message(_("Please disable windows screen curtain before using AI content describer."))
			return
		if focus:
			if self.prev_focus:
				nav = self.prev_focus
				self.prev_focus = None
			else:
				nav = api.getFocusObject()
		else:
			if self.prev_navigator:
				nav = self.prev_navigator
				self.prev_navigator = None
			else:
				nav = api.getNavigatorObject()
		notVisibleMsg = _("Content is not visible")
		try:
			left, top, width, height = nav.location
		except TypeError:
			log.debugWarning("Object returned location %r" % nav.location)
			ui.message(notVisibleMsg)
			return
		bounding_box = (left, top, left + width, top + height)
		snap = ImageGrab.grab(bounding_box)
		if not snap:
			# Translators: Message spoken when the attempt to take a picture of an object fails
			ui.message(_("Could not snap an image of the requested object"))
			return
		file = tempfile.mktemp(suffix=".png")
		snap.save(file)
		return threading.Thread(target=self.describe_image, kwargs={"file":file, "delete":True}).start()

	def describe_face(self):
		if not hasattr(self, "detection_interface"):
			error = getattr(self, "detection_interface_error", None)
			if error is not None:
				# py-3.11: On some machines, it is rare, but cv2 might not work as expected due to a variety of reasons none of which I can reproduce.
				## In the meantime, establish a catchall exception and report it to the user so they can file an issue
				# Translators: The message spoken when there was an error with the face detection interface.
				ui.message(_("Error initializing the face detection interface. Please consult the NVDA log for more information. "+error))
				return
			else:
				# Translators: Message spoken when the face detection interface is loading
				ui.message(_("Face detection interface is loading. Please try this command again after a couple seconds."))
				return
		return threading.Thread(target=self.detection_interface.run).start()

	def describe_screenshot(self):
		if self.is_screen_curtain_running():
			# Translators: message spoken when there is an attempt to recognize an object, but the screen curtain is running
			ui.message(_("Please disable windows screen curtain before using AI content describer."))
			return
		snap = ImageGrab.grab()
		if not snap:
			# translators: message spoken when grabbing the content of the current window is not possible
			ui.message(_("Could not get window content"))
			return
		file = tempfile.mktemp(suffix=".png")
		snap.save(file)
		return threading.Thread(target=self.describe_image, kwargs={"file":file, "delete":True}).start()

	def describe_camera(self):
		if not hasattr(self, "detection_interface"):
			error = getattr(self, "detection_interface_error", None)
			if error is not None:
				# py-3.11: On some machines, it is rare, but cv2 might not work as expected due to a variety of reasons none of which I can reproduce.
				## In the meantime, establish a catchall exception and report it to the user so they can file an issue
				# Translators: The message spoken when there was an error with the face detection interface.
				ui.message(_("Error initializing the face detection interface. Please consult the NVDA log for more information. "+error))
				return
			else:
				# Translators: Message spoken when the face detection interface is loading
				ui.message(_("Face detection interface is loading. Please try this command again after a couple seconds."))
				return
		self.detection_interface.run(process=False)
		if self.detection_interface.video_capture:
			success , frame = self.detection_interface.read_frame()
			if not success:
			# translators: message spoken when the picture could not be taken due to an unknown error
				ui.message(_("The picture could not be taken. Please ensure that your camera is not in use by another application and try again."))
				return
			file = tempfile.mktemp(suffix=".png")
			if not cv2.imwrite(file, frame):
				# Translators: the message spoken when the picture is taken but the file could not be written.
				ui.message(_("The picture could not be saved."))
				return
			return threading.Thread(target=self.describe_image, kwargs={"file":file, "delete":True}).start()
		else:
			# translators: message spoken when the picture could not be taken due to an unknown error
			ui.message(_("The picture could not be taken. Please ensure that your camera is not in use by another application and try again."))


	def describe_clipboard(self):
		snap = ImageGrab.grabclipboard()
		if isinstance(snap, list):
			if len(snap) == 0:
				# Translators: Message spoken when the item copied to the clipboard is not an image
				ui.message(_("The item on the clipboard is not an image."))
				return
			file = snap[0]
			if service.supported_formats and not os.path.splitext(file)[1].lower() in service.supported_formats:
				# Translators: Message spoken when the image on the clipboard is not a format supported by the current description service
				unsupported_format_msg = _("Unsupported image format. Please copy another file to the clipboard that is {formats}").format(formats=', '.join(service.supported_formats))
				ui.message(unsupported_format_msg)
				return
			return threading.Thread(target=self.describe_image, kwargs={"file":file, "delete":False}).start()
		elif not snap:
			# Translators: Message spoken when the item copied to the clipboard is not an image
			ui.message(_("The item on the clipboard is not an image."))
			return
		file = tempfile.mktemp(suffix=".png")
		snap.save(file, optimize=True, )
		return threading.Thread(target=self.describe_image, kwargs={"file":file, "delete":True}).start()

	def describe_image(self, file, delete=False):
		# Few sanity checks before we go ahead with the API request
		if not service.is_available:
			# Translators: Message spoken when the user attempts to describe something but they haven't yet provided an API key or base URL
			wx.CallAfter(ui.message, _("To describe content, you must provide an API key or base URL in the AI image describer category of the NVDA settings dialog. Please consult add-on help for more information"))
			return
		if not service.prompt:
			# Translators: Message spoken when a user attempts to describe something, but they haven't provided a prompt
			wx.CallAfter(ui.message, _("To describe content, you must define a prompt by navigating to the AI image describer category of the NVDA settings dialog. Please consult add-on help for more information"))
			return
		# Check whether an existing conversation dialog is open
		# If a conversation dialog is open, prompt to add the image and bring it to front
		# If delete is True, the file will automatically be cleaned up when the dialog is closed
		if offer_image_attachment(file, delete=delete):
			return
		tones.beep(300, 200)
		# Translators: Message spoken after the beep - when we have started fetching the description
		wx.CallAfter(ui.message, _("Retrieving description using {name}...").format(name=service.name))
		message = service.process(file, **ch.config[service.name])
		if ch.config["global"]["open_in_dialog"]:
			# Translators: Title of the browseable message
			messageTitle = _("Image description")
			try:
				message = markdown.markdown(message, extensions = [fenced_code.FencedCodeExtension(), tables.TableExtension(), nl2br.Nl2BrExtension(), sane_lists.SaneListExtension()])
			except Exception as e:
				log.exception("Exception while converting markdown to html, falling back to a text description")
			# The browsableMessage dialog uses mshtml, which doesn't appear to care if the text isn't actually markup.
			wx.CallAfter(ui.browseableMessage, message, messageTitle, True)
		else:
			wx.CallAfter(ui.message, message)
		if delete:
			log.debug("Cleaning up image: "+file)
			os.unlink(file)

	def show_area_menu(self):
		# Cache foreground HWND before prePopup steals focus
		import winUser
		foreground_hwnd = winUser.getForegroundWindow()
		self.prev_navigator = api.getNavigatorObject()
		self.prev_focus = api.getFocusObject()
		gui.mainFrame.prePopup()
		menu = AreaMenu()
		gui.mainFrame.PopupMenu(menu)
		menu.Destroy()
		gui.mainFrame.postPopup()
		# the focus and navigator objects change when a popup menu is opened and dismissed, so try to restore both
		# no matter whether focus can actually be set back to the object
		# this should also allow a cached response to be spoken before the form control
		api.setNavigatorObject(self.prev_navigator)
		api.setFocusObject(self.prev_focus)
		if menu.selection == menu.focus_item:
			self.describe_focus_object()
		elif menu.selection == menu.navigator_item:
			self.describe_navigator_object()
		elif menu.selection == menu.screenshot_item:
			self.describe_screenshot()
		elif menu.selection == menu.show_ui_item:
			computer_control.describe_ui(self, service)
		elif menu.selection == menu.camera_item:
			self.describe_camera()
		elif menu.selection == menu.detect_face_item:
			self.describe_face()
		elif menu.selection == menu.select_camera_item:
			self.detection_interface.show_device_dialog_if_needed(force=True)
		elif menu.selection == menu.release_camera_item:
			self.detection_interface.destroy()
			# translators: message spoken after the camera has been released successfully
			ui.message(_("Success"))
		elif menu.selection == menu.followup_item and menu.followup_item is not None:
			self.show_conversation_dialog()
		elif menu.selection == menu.computer_use_item:
			self.open_computer_control_session(foreground_hwnd)
		else:
			self.prev_focus = None
			self.prev_navigator = None

	def show_conversation_dialog(self):
		"""Show the conversation dialog for multi-modal interaction."""
		if not service or not service.has_conversation():
			# translators: The message spoken when the user attempts to show the conversation dialog, but no service is available.
			ui.message(_("No AI service or conversation available."))
			return
		return launch_conversation_dialog(service, gui.mainFrame)

	def script_show_conversation(self, gesture):
		return self.show_conversation_dialog()
	script_show_conversation.__doc__ = _("Open the AI conversation dialog for follow-up questions and multimodal chat.")

	def script_describe_clipboard(self, gesture):
		self.describe_clipboard()
	script_describe_clipboard.__doc__ = _("Describe the image (or file path to an image) on the clipboard using AI.")

	def script_describe_navigator(self, gesture):
		self.describe_navigator_object()
	script_describe_navigator.__doc__ = _("Describe the contents of the current navigator object using AI.")

	def script_describe_focus(self, gesture):
		self.describe_focus_object()
	script_describe_focus.__doc__ = _("Describe the contents of the currently focused item using AI.")

	def script_describe_screenshot(self, gesture):
		self.describe_screenshot()
	script_describe_screenshot.__doc__ = _("Take a screenshot, then describe it using AI.")

	def script_describe_image(self, gesture):
		wx.CallAfter(self.show_area_menu)
	script_describe_image.__doc__ = _("Pop up a menu asking whether to describe the current focus, navigator object, or entire screen with AI.")

	def open_computer_control_session(self, hwnd):
		if not service:
			ui.message(_("No AI service configured."))
			return
		if not service.supports_computer_use:
			ui.message(_("Computer use is not supported by the selected model."))
			return
		if self.is_screen_curtain_running():
			ui.message(_("Computer control cannot be used while the screen curtain is active."))
			return
		cancel_event = threading.Event()
		pause_event = threading.Event()
		dlg = MultimodalInput(service, gui.mainFrame, mode="computer_use")
		def on_message(text, role):
			dlg.append_message(text, role=role)
		def on_first_message(task):
			session = ComputerUseSession(
				service=service,
				hwnd=hwnd,
				on_message=on_message,
				cancel_event=cancel_event,
				pause_event=pause_event,
				request_approval=_show_computer_use_approval,
				dialog=dlg,
			)
			dlg._computer_use_session = session
			dlg._cancel_event = cancel_event
			# Hand the foreground to the user's window and get our dialog out of
			# the way before the session screenshots or sends any input.
			import winUser
			winUser.setForegroundWindow(hwnd)
			dlg.Hide()
			tones.beep(1000, 300)
			session.start(task)
		dlg.on_first_message_callback = on_first_message
		dlg.Show()

	def script_pause_resume_computer_use(self, gesture):
		for win in wx.GetTopLevelWindows():
			if hasattr(win, "_computer_use_session"):
				session = win._computer_use_session
				if session._pause_event.is_set():
					session._pause_event.clear()
					tones.beep(1000, 300)
					# Translators: spoken when a computer control session is resumed
					ui.message(_("Computer control resumed."))
				else:
					session._pause_event.set()
					# Translators: spoken when a computer control session is paused
					ui.message(_("Computer control paused."))
					tones.beep(108, 300)
				return
		# Translators: spoken when the pause gesture is pressed but no session is running
		ui.message(_("No active computer control session."))

	script_pause_resume_computer_use.__doc__ = _("Pause or resume the active computer control session")

	def script_cancel_computer_use(self, gesture):
		for win in wx.GetTopLevelWindows():
			if hasattr(win, "_computer_use_session"):
				win._computer_use_session._cancel_event.set()
				# Translators: spoken when the user cancels a computer control session
				ui.message(_("Computer control session cancelled."))
				return
		ui.message(_("No active computer control session."))

	script_cancel_computer_use.__doc__ = _("Cancel the active computer control session")

	def script_describe_camera(self, gesture):
		self.describe_camera()
	script_describe_camera.__doc__ = _("Snap a picture using the selected camera, then describe it using AI.")

	def script_describe_face(self, gesture):
		self.describe_face()
	script_describe_face.__doc__ = _("Describe the position of the face in the frame using the selected camera, if applicable.")

	def is_screen_curtain_running(self):
		import vision
		# Prior to NVDA 2026.1, Screen Curtain was a visionEnhancementProvider. We need to account for this
		legacy_api = False
		try:
			from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider
			legacy_api = True
		except ModuleNotFoundError:
			from screenCurtain import screenCurtain
		if legacy_api:
			screenCurtainId = ScreenCurtainProvider.getSettings().getId()
			screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
			return bool(vision.handler.getProviderInstance(screenCurtainProviderInfo))
		return screenCurtain is not None and screenCurtain.enabled



	__gestures = {
		"kb:shift+NVDA+i": "describe_image",
		"kb:shift+NVDA+u": "describe_navigator",
		"kb:shift+NVDA+y": "describe_clipboard",
		"kb:shift+NVDA+j": "describe_face",
		"kb:alt+NVDA+c": "show_conversation",
		"kb:NVDA+control+shift+p": "pause_resume_computer_use",
	}

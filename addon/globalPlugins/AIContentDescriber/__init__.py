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
#addonHandler.initTranslation()
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
from PIL import ImageGrab
import config_handler as ch
from description_service import GPT4
sys.path.remove(sys.path[-1])

service = None


class AIDescriberSettingsPanel(SettingsPanel):
	# Translators: The label for the category in NVDA settings
	title = _("AI Content Describer")

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: The label for the API key field in in the settings dialog
		self.api_key = sHelper.addLabeledControl(_("OpenAI API key"), wx.TextCtrl)
		# Translators: The label for the prompt field in the settings dialog
		self.prompt = sHelper.addLabeledControl(_("Prompt"), wx.TextCtrl, style=wx.TE_MULTILINE)
		# Translators: The label for the button that resets the prompt to its default in the settings dialog
		self.reset_prompt = sHelper.addItem(wx.Button(self, label=_("Reset prompt to default")))
		# Translators: The label for the maximum tokens chooser in the settings dialog
		self.max_tokens = sHelper.addLabeledControl(_("Maximum tokens"), nvdaControls.SelectOnFocusSpinCtrl, min=1, max=1000)
		# Translators: The label for the option to open results in browseable dialogs
		self.open_in_dialog = sHelper.addItem(wx.CheckBox(self, label=_("Open each result in a browseable dialog")))
		# Translators: The label for the checkbox to cash images and their descriptions in the settings dialog
		self.cache_descriptions = sHelper.addItem(wx.CheckBox(self, label=_("Remember/cache descriptions of each item to save API quota")))
		# Translators: The label for the timeout chooser in the settings dialog
		self.timeout = sHelper.addLabeledControl("Seconds to wait for a response before timing out", nvdaControls.SelectOnFocusSpinCtrl, min=1)
		# Translators: The label for the checkbox that controls whether to optimize image uploads for size in the settings dialog
		self.optimize_for_size = sHelper.addItem(wx.CheckBox(self, label="Optimize images for size, may speed up detection in some situations (experimental)"))
		self.bind_events()
		self.populate_values()

	def bind_events(self):
		self.Bind(wx.EVT_BUTTON, self.on_prompt_reset, self.reset_prompt)

	def populate_values(self):
		self.api_key.SetValue(ch.config[service.name]["api_key"])
		self.prompt.SetValue(ch.config[service.name]["prompt"])
		self.max_tokens.SetValue(ch.config[service.name]["max_tokens"])
		self.cache_descriptions.SetValue(ch.config[service.name]["cache_descriptions"])
		self.timeout.SetValue(ch.config[service.name]["timeout"])
		self.open_in_dialog.SetValue(ch.config[service.name]["open_in_dialog"])
		self.optimize_for_size.SetValue(ch.config[service.name]["optimize_for_size"])

	def onSave(self):
		ch.config[service.name]["api_key"] = self.api_key.GetValue()
		ch.config[service.name]["prompt"] = self.prompt.GetValue()
		ch.config[service.name]["max_tokens"] = self.max_tokens.GetValue()
		ch.config[service.name]["cache_descriptions"] = self.cache_descriptions.GetValue()
		ch.config[service.name]["timeout"] = self.timeout.GetValue()
		ch.config[service.name]["optimize_for_size"] = self.optimize_for_size.GetValue()
		ch.config[service.name]["open_in_dialog"] = self.open_in_dialog.GetValue()
		ch.config.write()

	def on_prompt_reset(self, event):
		self.prompt.SetValue(service.DEFAULT_PROMPT)
		self.prompt.SetFocus()


class AreaMenu(wx.Menu):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.selection = None
		# translators: current focus
		self.focus_item = self.Append(wx.ID_ANY, "Current focus")
		# translators: navigator object
		self.navigator_item = self.Append(wx.ID_ANY, "Navigator object")
		# translators: screenshot of entire window menu item
		self.screenshot_item = self.Append(wx.ID_ANY, "Entire screen")
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.focus_item)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.navigator_item)
		gui.mainFrame.Bind(wx.EVT_MENU, self.on_menu_selected, self.screenshot_item)

	def on_menu_selected(self, event):
		self.selection = self.FindItemById(event.GetId())


class GlobalPlugin(GlobalPlugin):
	scriptCategory = _("AI Content Describer")

	def __init__(self, *args, **kwargs):
		global service
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(AIDescriberSettingsPanel)
		ch.load_config()
		service = GPT4()
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

	def describe_screenshot(self):
		snap = ImageGrab.grab()
		if not snap:
			# translators: message spoken when grabbing the content of the current window is not possible
			ui.message(_("Could not get window content"))
			return
		file = tempfile.mktemp(suffix=".png")
		snap.save(file)
		return threading.Thread(target=self.describe_image, kwargs={"file":file, "delete":True}).start()

	def describe_clipboard(self):
		snap = ImageGrab.grabclipboard()
		if isinstance(snap, list):
			if len(snap) == 0:
				# Translators: Message spoken when the item copied to the clipboard is not an image
				ui.message(_("The item on the clipboard is not an image."))
				return
			file = snap[0]
			if service.supported_formats and not os.path.splitext(file)[1] in service.supported_formats:
				# Translators: Message spoken when the image on the clipboard is not a format supported by the current description service
				unsupported_format_msg = _(f"Unsupported image format. Please copy another file to the clipboard that is {''.join(service.supported_formats)}")
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
		if not ch.config[service.name]["api_key"]:
			# Translators: Message spoken when the user attempts to describe something but they haven't yet provided an API key
			ui.message(_("To describe content, you must provide an API key in the AI image describer category of the NVDA settings dialog. Please consult add-on help for more information"))
			return
		if not ch.config[service.name]["prompt"]:
			# Translators: Message spoken when a user attempts to describe something, but they haven't provided a prompt
			ui.message(_("To describe content, you must define a prompt by navigating to the AI image describer category of the NVDA settings dialog. Please consult add-on help for more information"))
			return
		tones.beep(300, 200)
		# Translators: Message spoken after the beep - when we have started fetching the description
		ui.message(_("Retrieving description..."))
		message = service.process(file, **ch.config[service.name])
		if ch.config[service.name]["open_in_dialog"]:
			# Translators: Title of the browseable message
			wx.CallAfter(ui.browseableMessage, message, _("Image description"))
		else:
			ui.message(message)
		if delete:
			os.unlink(file)

	def show_area_menu(self):
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
		else:
			self.prev_focus = None
			self.prev_navigator = None

	def script_describe_clipboard(self, gesture):
		"""Describe the image (or file path to an image) on the clipboard using AI."""
		self.describe_clipboard()

	def script_describe_navigator(self, gesture):
		"""Describe the contents of the current navigator object using AI."""
		self.describe_navigator_object()

	def script_describe_focus(self, gesture):
		"""Describe the contents of the currently focused item using AI."""
		self.describe_focus_object()

	def script_describe_screenshot(self, gesture):
		"""Take a screenshot, then describe it using AI."""
		self.describe_screenshot()

	def script_describe_image(self, gesture):
		"""Pop up a menu asking whether to describe the current focus, navigator object, or entire screen with AI."""
		wx.CallAfter(self.show_area_menu)

	def is_screen_curtain_running(self):
		import vision
		from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider
		screenCurtainId = ScreenCurtainProvider.getSettings().getId()
		screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
		return bool(vision.handler.getProviderInstance(screenCurtainProviderInfo))

	__gestures = {
		"kb:shift+NVDA+i": "describe_image",
		"kb:shift+NVDA+u": "describe_navigator",
		"kb:shift+NVDA+y": "describe_clipboard",
	}

import wx
from gui import guiHelper
from gui import nvdaControls
from gui import settingsDialogs
import addonHandler
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Couldn't initialise translations. Is this addon running from NVDA's scratchpad directory?")

import description_service


class ModelsDialog(settingsDialogs.MultiCategorySettingsDialog):
	# translators: the title of the model configuration dialog.
	title = _("Model configuration")
	categoryClasses = []
	parent = None


class BaseModelSettingsPanel(settingsDialogs.SettingsPanel):
	model = None
	def makeSettings(self, settingsSizer):
		self.bind_events()
		self.populate_values()

	def add_about_button(self, sHelper):
		# translators: the button in the model configuration dialog that provides information on the selected model
		self.about_button = sHelper.addItem(wx.Button(self, label=_("About this model")))

	def add_api_key_field(self, sHelper):
		# Translators: The label for the API key field in the model configuration dialog
		self.api_key = sHelper.addLabeledControl(_(f"API key"), wx.TextCtrl)

	def add_base_url_field(self, sHelper):
		# Translators: The label for the base URL field in the model configuration dialog
		self.base_url = sHelper.addLabeledControl(_(f"Base URL"), wx.TextCtrl)

	def add_prompt_field(self, sHelper):
		# Translators: The label for the prompt field in the model configuration dialog
		self.prompt = sHelper.addLabeledControl(_("Prompt"), wx.TextCtrl, style=wx.TE_MULTILINE)
		# Translators: The label for the button that resets the prompt to its default in the settings dialog
		self.reset_prompt = sHelper.addItem(wx.Button(self, label=_("Reset prompt to default")))

	def add_max_tokens_field(self, sHelper):
		# Translators: The label for the maximum tokens chooser in the model configuration dialog
		self.max_tokens = sHelper.addLabeledControl(_("Maximum tokens"), nvdaControls.SelectOnFocusSpinCtrl, min=1, max=1000)

	def add_timeout_field(self, sHelper):
		# Translators: The label for the timeout chooser in the model configuration dialog
		self.timeout = sHelper.addLabeledControl(_("Seconds to wait for a response before timing out"), nvdaControls.SelectOnFocusSpinCtrl, min=1)

	def populate_values(self):
		if hasattr(self, "api_key"):
			self.api_key.SetValue(self.model.api_key)
		if hasattr(self, "base_url"):
			self.base_url.SetValue(self.model.base_url)
		if hasattr(self, "prompt"):
			self.prompt.SetValue(self.model.prompt)
		if hasattr(self, "max_tokens"):
			self.max_tokens.SetValue(self.model.max_tokens)
		if hasattr(self, "timeout"):
			self.timeout.SetValue(self.model.timeout)

	def onSave(self):
		if hasattr(self, "api_key"):
			self.model.api_key = self.api_key.GetValue()
		if hasattr(self, "base_url"):
			self.model.base_url = self.base_url.GetValue()
		if hasattr(self, "prompt"):
			self.model.prompt = self.prompt.GetValue()
		if hasattr(self, "max_tokens"):
			self.model.max_tokens = self.max_tokens.GetValue()
		if hasattr(self, "timeout"):
			self.model.timeout = self.timeout.GetValue()
		self.model.save_config()
		if models_dialog_parent is not None:
				models_dialog_parent.populate_values()  # mainly to refresh the list of available models

	def bind_events(self):
		if hasattr(self, "reset_prompt"):
			self.Bind(wx.EVT_BUTTON, self.on_prompt_reset, self.reset_prompt)
		if hasattr(self, "about_button"):
			self.Bind(wx.EVT_BUTTON, self.on_about, self.about_button)

	def on_prompt_reset(self, event):
		self.prompt.SetValue(self.model.DEFAULT_PROMPT)
		self.prompt.SetFocus()

	def on_about(self, event):
		wx.MessageBox(
			# translators: the title for the about model message box
			caption=_("About model"),
			message=self.model.description,
			style=wx.ICON_INFORMATION|wx.CENTER
		)


class GPT4ConfigurationPanel(BaseModelSettingsPanel):
	model = description_service.GPT4()
	title = model.name
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.add_about_button(sHelper)
		self.add_api_key_field(sHelper)
		self.add_prompt_field(sHelper)
		self.add_max_tokens_field(sHelper)
		self.add_timeout_field(sHelper)
		super().makeSettings(settingsSizer)


class GPT4TurboConfigurationPanel(GPT4ConfigurationPanel):
	model = description_service.GPT4Turbo()
	title = model.name


class GeminiConfigurationPanel(BaseModelSettingsPanel):
	model = description_service.Gemini()
	title = model.name
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.add_about_button(sHelper)
		self.add_api_key_field(sHelper)
		self.add_prompt_field(sHelper)
		self.add_max_tokens_field(sHelper)
		self.add_timeout_field(sHelper)
		super().makeSettings(settingsSizer)


class LlamaCPPConfigurationPanel(BaseModelSettingsPanel):
	model = description_service.LlamaCPP()
	title = model.name + " (unstable)"
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.add_about_button(sHelper)
		self.add_base_url_field(sHelper)
		self.add_prompt_field(sHelper)
		self.add_max_tokens_field(sHelper)
		self.add_timeout_field(sHelper)
		super().makeSettings(settingsSizer)


class ClaudeConfigurationPanel(BaseModelSettingsPanel):
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.add_about_button(sHelper)
		self.add_api_key_field(sHelper)
		self.add_prompt_field(sHelper)
		self.add_max_tokens_field(sHelper)
		self.add_timeout_field(sHelper)
		super().makeSettings(settingsSizer)


class Claude3OpusConfigurationPanel(ClaudeConfigurationPanel):
	model = description_service.Claude3Opus()
	title = model.name


class Claude3SonnetConfigurationPanel(ClaudeConfigurationPanel):
	model = description_service.Claude3Sonnet()
	title = model.name


class Claude3HaikuConfigurationPanel(ClaudeConfigurationPanel):
	model = description_service.Claude3Haiku()
	title = model.name


description_service.GPT4.configurationPanel = GPT4ConfigurationPanel
description_service.GPT4Turbo.configurationPanel = GPT4TurboConfigurationPanel
description_service.Gemini.configurationPanel = GeminiConfigurationPanel
description_service.LlamaCPP.configurationPanel = LlamaCPPConfigurationPanel
description_service.Claude3Haiku.configurationPanel = Claude3HaikuConfigurationPanel
description_service.Claude3Sonnet.configurationPanel = Claude3SonnetConfigurationPanel
description_service.Claude3Opus.configurationPanel = Claude3OpusConfigurationPanel
models_dialog_parent = None


def build_model_configuration_dialog(parent=None):
	global models_dialog_parent  # I don't prefer doing this, but it's easier than fetching it on the fly
	dlg = ModelsDialog
	models_dialog_parent = parent
	for model in description_service.models:
		if hasattr(model, "configurationPanel"):
			panel = model.configurationPanel
			if not panel in dlg.categoryClasses:
				dlg.categoryClasses.append(panel)
	return dlg

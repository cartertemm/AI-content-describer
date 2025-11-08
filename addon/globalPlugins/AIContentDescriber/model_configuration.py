import threading
import wx
from gui import guiHelper
from gui import nvdaControls
from gui import settingsDialogs
import addonHandler
import logHandler
log = logHandler.log

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

	def add_model_name_field(self, sHelper):
		# Translators: The label for the model name field in the model configuration dialog
		self.chosen_model = sHelper.addLabeledControl(_(f"Model name"), wx.TextCtrl)

	def add_list_models_button(self, sHelper):
		# Translators: The label for the list models button in the model configuration dialog
		self.list_models_button = sHelper.addItem(wx.Button(self, label=_("List models")))

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
		if hasattr(self, "chosen_model"):
			self.chosen_model.SetValue(self.model.chosen_model)
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
		if hasattr(self, "chosen_model"):
			self.model.chosen_model = self.chosen_model.GetValue()
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
		if hasattr(self, "list_models_button"):
			self.Bind(wx.EVT_BUTTON, self.on_list_models, self.list_models_button)

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

	def on_list_models(self, event):
		base_url = self.base_url.GetValue()
		if self.model.needs_base_url and not base_url:
			self.base_url.SetFocus()
			return
		self.models = self.model.list_model_names(self.base_url.GetValue())
		if len(self.models) == 0:
			# Translators: The message spoken when there were no models found.
			import ui
			ui.message(_("No models were found. Please install one, then try again."))
			return
		dlg = ModelListDialog(self)
		dlg.ShowModal()
		self.chosen_model.SetFocus()


class ModelListDialog(settingsDialogs.SettingsDialog):
	# Translators: the label for the list models dialog
	title = _("Select a model")
	models = []
	def postInit(self):
		self.models_list.SetFocus()

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: Label of the model combo box in the choose model dialog
		label = _("Model:")
		self.models_list = sHelper.addLabeledControl(label, wx.Choice, choices=[])
		self.update_models_list()

	def update_models_list(self):
		self.models_list.Clear()
		chosen_model = self.Parent.chosen_model.GetValue()
		self.models_list.AppendItems(self.Parent.models)
		try:
			index = self.Parent.models.index(chosen_model)
			self.models_list.SetSelection(index)
		except:
			pass

	def onOk(self, event):
		if not self.Parent.models:
			return
		parent = self.GetParent()
		model_selection = self.models_list.GetStringSelection()
		if model_selection:
			parent.chosen_model.SetValue(model_selection)
		super().onOk(event)


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


class GPT4OConfigurationPanel(GPT4ConfigurationPanel):
	model = description_service.GPT4O()
	title = model.name

class GPT41ConfigurationPanel(GPT4ConfigurationPanel):
	model = description_service.GPT41()
	title = model.name

class GPT5ChatConfigurationPanel(GPT4ConfigurationPanel):
	model = description_service.GPT5Chat()
	title = model.name


class O4MiniConfigurationPanel(GPT4ConfigurationPanel):
	model = description_service.O4Mini()
	title = model.name


class O3ConfigurationPanel(GPT4ConfigurationPanel):
	model = description_service.O3()
	title = model.name


class O3MiniConfigurationPanel(GPT4ConfigurationPanel):
	model = description_service.O3Mini()
	title = model.name


class O3ProConfigurationPanel(GPT4ConfigurationPanel):
	model = description_service.O3Pro()
	title = model.name


class PollinationsAIConfigurationPanel(BaseModelSettingsPanel):
	model = description_service.PollinationsAI()
	title = model.name
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.add_about_button(sHelper)
		self.add_prompt_field(sHelper)
		self.add_max_tokens_field(sHelper)
		self.add_timeout_field(sHelper)
		super().makeSettings(settingsSizer)


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


class GeminiFlash1_5_8BConfigurationPanel(GeminiConfigurationPanel):
	model = description_service.GeminiFlash1_5_8B()
	title = model.name


class Gemini1_5ProConfigurationPanel(GeminiConfigurationPanel):
	model = description_service.Gemini1_5Pro()
	title = model.name


class Gemini2_0FlashLitePreviewConfigurationPanel(GeminiConfigurationPanel):
	model = description_service.Gemini2_0FlashLitePreview()
	title = model.name


class Gemini2_0FlashConfigurationPanel(GeminiConfigurationPanel):
	model = description_service.Gemini2_0Flash()
	title = model.name


class Gemini2_5FlashPreviewConfigurationPanel(GeminiConfigurationPanel):
	model = description_service.Gemini2_5FlashPreview()
	title = model.name


class Gemini2_5ProPreviewConfigurationPanel(GeminiConfigurationPanel):
	model = description_service.Gemini2_5ProPreview()
	title = model.name


class MistralAIConfigurationPanel(BaseModelSettingsPanel):
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.add_about_button(sHelper)
		self.add_api_key_field(sHelper)
		self.add_prompt_field(sHelper)
		self.add_max_tokens_field(sHelper)
		self.add_timeout_field(sHelper)
		super().makeSettings(settingsSizer)


class PixtralLargeConfigurationPanel(MistralAIConfigurationPanel):
	model = description_service.PixtralLarge()
	title = model.name


class VivoBlueLMVisionConfigurationPanel(BaseModelSettingsPanel):
	model = description_service.VivoBlueLMVision()
	title = model.name

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.add_about_button(sHelper)
		# Translators: The label for the NVDA-CN username field.
		self.nvdacn_user = sHelper.addLabeledControl(_("NVDA-CN Username"), wx.TextCtrl)
		# Translators: The label for the NVDA-CN password field.
		self.nvdacn_pass = sHelper.addLabeledControl(_("NVDA-CN Password"), wx.TextCtrl, style=wx.TE_PASSWORD)
		self.add_prompt_field(sHelper)
		self.add_timeout_field(sHelper)
		super().makeSettings(settingsSizer)

	def populate_values(self):
		self.nvdacn_user.SetValue(self.model.nvdacn_user or "")
		self.nvdacn_pass.SetValue(self.model.nvdacn_pass or "")
		super().populate_values()

	def onSave(self):
		self.model.nvdacn_user = self.nvdacn_user.GetValue()
		self.model.nvdacn_pass = self.nvdacn_pass.GetValue()
		super().onSave()


class OllamaConfigurationPanel(BaseModelSettingsPanel):
	model = description_service.Ollama()
	# Translators: Requires installation
	title = model.name + _(" (requires installation)")
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.add_about_button(sHelper)
		self.add_base_url_field(sHelper)
		self.add_model_name_field(sHelper)
		self.add_list_models_button(sHelper)
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


class Claude3_5SonnetConfigurationPanel(ClaudeConfigurationPanel):
	model = description_service.Claude3_5Sonnet()
	title = model.name

class Claude3_5HaikuConfigurationPanel(ClaudeConfigurationPanel):
	model = description_service.Claude3_5Haiku()
	title = model.name


class Claude3_5SonnetV2ConfigurationPanel(ClaudeConfigurationPanel):
	model = description_service.Claude3_5SonnetV2()
	title = model.name


class Claude3_7SonnetConfigurationPanel(ClaudeConfigurationPanel):
	model = description_service.Claude3_7Sonnet()
	title = model.name


class Claude4OpusConfigurationPanel(ClaudeConfigurationPanel):
	model = description_service.Claude4Opus()
	title = model.name


class Claude4SonnetConfigurationPanel(ClaudeConfigurationPanel):
	model = description_service.Claude4Sonnet()
	title = model.name




class Grok2VisionConfigurationPanel(BaseModelSettingsPanel):
	model = description_service.Grok2Vision()
	title = model.name
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.add_about_button(sHelper)
		self.add_api_key_field(sHelper)
		self.add_prompt_field(sHelper)
		self.add_max_tokens_field(sHelper)
		self.add_timeout_field(sHelper)
		super().makeSettings(settingsSizer)


description_service.PollinationsAI.configurationPanel = PollinationsAIConfigurationPanel
description_service.GPT4.configurationPanel = GPT4ConfigurationPanel
description_service.O4Mini.configurationPanel = O4MiniConfigurationPanel
description_service.O3.configurationPanel = O3ConfigurationPanel
description_service.O3Mini.configurationPanel = O3MiniConfigurationPanel
description_service.O3Pro.configurationPanel = O3ProConfigurationPanel
description_service.GPT4Turbo.configurationPanel = GPT4TurboConfigurationPanel
description_service.GPT4O.configurationPanel = GPT4OConfigurationPanel
description_service.GPT41.configurationPanel = GPT41ConfigurationPanel
description_service.GPT5Chat.configurationPanel = GPT5ChatConfigurationPanel
description_service.Gemini2_0FlashLitePreview.configurationPanel = Gemini2_0FlashLitePreviewConfigurationPanel
description_service.Gemini2_0Flash.configurationPanel = Gemini2_0FlashConfigurationPanel
description_service.Gemini.configurationPanel = GeminiConfigurationPanel
description_service.GeminiFlash1_5_8B.configurationPanel = GeminiFlash1_5_8BConfigurationPanel
description_service.Gemini1_5Pro.configurationPanel = Gemini1_5ProConfigurationPanel
description_service.PixtralLarge.configurationPanel = PixtralLargeConfigurationPanel
description_service.VivoBlueLMVision.configurationPanel = VivoBlueLMVisionConfigurationPanel # <-- 在这里添加
description_service.Ollama.configurationPanel = OllamaConfigurationPanel
description_service.LlamaCPP.configurationPanel = LlamaCPPConfigurationPanel
description_service.Claude3_5Sonnet.configurationPanel = Claude3_5SonnetConfigurationPanel
description_service.Claude3Haiku.configurationPanel = Claude3HaikuConfigurationPanel
description_service.Claude3Sonnet.configurationPanel = Claude3SonnetConfigurationPanel
description_service.Claude3Opus.configurationPanel = Claude3OpusConfigurationPanel
description_service.Grok2Vision.configurationPanel = Grok2VisionConfigurationPanel
description_service.Gemini2_5FlashPreview.configurationPanel = Gemini2_5FlashPreviewConfigurationPanel
description_service.Gemini2_5ProPreview.configurationPanel = Gemini2_5ProPreviewConfigurationPanel
description_service.Claude4Opus.configurationPanel = Claude4OpusConfigurationPanel
description_service.Claude4Sonnet.configurationPanel = Claude4SonnetConfigurationPanel
description_service.Claude3_7Sonnet.configurationPanel = Claude3_7SonnetConfigurationPanel
description_service.Claude3_5Haiku.configurationPanel = Claude3_5HaikuConfigurationPanel
description_service.Claude3_5SonnetV2.configurationPanel = Claude3_5SonnetV2ConfigurationPanel
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

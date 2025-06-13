# Adding a New Description Service to AI Content Describer

This guide explains how to add a new AI description service, or model, to the AI Content Describer NVDA add-on. Assuming you have gathered details on the new model and can write basic Python, you just need to modify three files.

## At a glance

The process follows this pattern:

1. Create your service class in `description_service.py`, inherriting from the base class that best matches your service's capabilities and response format
2. Add it to the models list at the bottom of the same file. The order here is preserved in the settings dialog, so please be diligent. Best practice is to group all models from the same provider together, sorted by recency and relevance
3. Create a configuration panel in `model_configuration.py`, again inherriting from the base class that makes sense
4. Assign the panel to your service
5. Add the configuration section to `configspec.py`

Specific steps are as follows.

## Step-by-Step Instructions

### Step 1: Choose or Create a Base Class in `description_service.py`

First, determine if your new service can use an existing base class or needs a new one.

#### Option A: Use an Existing Base Class

If your service is compatible with an existing API format, inherit from the appropriate base class:

- **`BaseGPT`**: For anything compatible with the OpenAI API format (most common). Even if your service doesn't match this spec exactly, check to see if there is a "/openai" endpoint or similar
- **`GoogleGemini`**: For Google's Gemini API format
- **`Anthropic`**: For Claude/Anthropic API format
- **`BaseDescriptionService`**: For completely custom implementations

#### Option B: Create a New Base Class

If your service uses a unique API format that we haven't seen before, create a new base class by inheriting from `BaseDescriptionService` and overriding these methods:

```python
class YourProviderBase(BaseDescriptionService):
	def build_conversation_payload(self, messages, **kw):
		"""Convert messages from an OpenAI style format to the one used by your provider"""
		pass

	def _get_conversation_headers(self):
		"""Return headers for API requests"""
		pass

	def _get_conversation_url(self):
		"""Return the API endpoint URL"""
		pass

	def _extract_conversation_response(self, response_json):
		"""Extract and return a string containing the AI response from the API response JSON.
		This should also handle errors gracefully, i.e. `ui.message`."""
		pass
```

### Step 2: Create Your Service Class

Add your new service class to `description_service.py`:

```python
class YourNewService(BaseGPT):  # or appropriate base class
	name = "Your Service Name"  # This MUST match the section name in configspec.py
	description = _("Description shown in the about dialog")
	about_url = "https://example.com/docs"
	internal_model_name = "actual-model-name-used-in-api"

	# the following properties can be omitted if not applicable
	DEFAULT_PROMPT = ""
	supported_formats = [".jpeg", ".jpg", ".png", ".webp", ".gif"]
	needs_api_key = True
	needs_base_url = False
	needs_configuration_dialog = True

	# Add the @cached_description decorator to enable caching
	@cached_description
	def process(self, image_path, **kw):
		# Your implementation here, consult other providers to see how this works.
		# This method takes the path to an image, and a dictionary of keyword arguments that mirror the configuration section for this service.
		# It should construct the list of messages, build the payload, start the multimodal conversation in memory, and then return the description string
		base64_image = encode_image(image_path)
		messages = [{
			"role": "user",
			"content": self.prompt,
			"image": base64_image
		}]
		payload = self.build_conversation_payload(messages)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(...)
		response_json = json.loads(response.decode('utf-8'))
		content = self._extract_conversation_response(response_json)
		if not content:
			return
		self.start_conversation(image_path, self.prompt, content)
		return content
```

### Step 3: Add Your Service to the Models List

At the bottom of `description_service.py`, add your service to the `models` list in the order you want it to appear in the UI:

```python
models = [
	PollinationsAI(),
	GPT4O(),
	# ... existing models ...
	YourNewService(),  # Add your service here
	Ollama(),
	LlamaCPP(),
]
```

### Step 4: Create a Configuration Panel in `model_configuration.py`

Create a configuration panel class for your service:

```python
class YourNewServiceConfigurationPanel(BaseModelSettingsPanel):  # or appropriate base
	model = description_service.YourNewService()
	title = model.name

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Add configuration fields based on your service's requirements
		self.add_about_button(sHelper)
		if self.model.needs_api_key:
			self.add_api_key_field(sHelper)
		if self.model.needs_base_url:
			self.add_base_url_field(sHelper)
		# Standard fields most services need
		self.add_prompt_field(sHelper)
		self.add_max_tokens_field(sHelper)
		self.add_timeout_field(sHelper)
		# For services like Ollama that support multiple models
		if hasattr(self.model, 'list_model_names'):
			self.add_model_name_field(sHelper)
			self.add_list_models_button(sHelper)
		super().makeSettings(settingsSizer)
```

### Step 5: Assign the Configuration Panel

At the bottom of `model_configuration.py`, assign your panel to your service:

```python
description_service.YourNewService.configurationPanel = YourNewServiceConfigurationPanel
```

### Step 6: Add Configuration Section to `configspec.py`

Add a configuration section using the **exact same name** as your service's `name` property (in the class you created in `description_service.py`):

```python
[Your Service Name]  # This MUST match your service's name property exactly
api_key = string(default="")  # Include if needs_api_key = True
base_url = string(default="")  # Include if needs_base_url = True
chosen_model = string(default="")  # Include if service supports multiple models
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)
```

## Available Configuration Fields

### Common Fields for BaseModelSettingsPanel

- **`add_about_button(sHelper)`**: Adds an "About" button that shows the model description
- **`add_api_key_field(sHelper)`**: Text field for API key (use if `needs_api_key = True`)
- **`add_base_url_field(sHelper)`**: Text field for base URL (use if `needs_base_url = True`)
- **`add_model_name_field(sHelper)`**: Text field for model name (for services supporting multiple models)
- **`add_list_models_button(sHelper)`**: Button to fetch available models (requires implementing `list_model_names()`)
- **`add_prompt_field(sHelper)`**: Multi-line text field for the prompt
- **`add_max_tokens_field(sHelper)`**: Spin control for maximum tokens
- **`add_timeout_field(sHelper)`**: Spin control for request timeout

## Special Considerations

### Services Without API Keys

For services that don't require API keys (like Pollinations or local services):

```python
needs_api_key = False
```

### Services with Multiple Models

For services like Ollama that support multiple models, implement the `list_model_names()` method:

```python
def list_model_names(self, base_url):
	# Implementation to fetch available models
	# Return a list of model names
	pass
```

### Custom API Formats

If your service uses a different API format, override the conversation methods:

```python
def build_conversation_payload(self, messages, **kw):
	"""Convert the standard message format, which follows OpenAI, to your API's format"""
	pass

def _extract_conversation_response(self, response_json):
	"""Extract the response text from your API's response format"""
	pass
```

## Testing Your Implementation

1. **Configuration**: Verify your service appears in the model configuration dialog
2. **Settings**: Test that all configuration fields save and load properly
3. **API Calls**: Test image description functionality
4. **Conversations**: Test follow-up conversation functionality
5. **Error Handling**: Test behavior with invalid API keys, network errors, etc. Ensure that the problem is announced after the beep, preferably with actionable steps to help the user fix it

## Example: Adding a Hypothetical "VisionAI" Service

Here's a complete example of adding a fictional service based on the OpenAI API format:

### In `description_service.py`:

```python
class VisionAI(BaseGPT):
	name = "VisionAI Pro"
	# translators: The description of the VisionAI Pro model in the model configuration dialog.
	description = _("Advanced vision AI with superior image understanding capabilities")
	about_url = "https://visionai.example.com/docs"
	internal_model_name = "vision-pro-v2"

	def _get_conversation_url(self):
		return "https://api.visionai.com/v1/describe"

# Add to models list
models = [
	PollinationsAI(),
	VisionAI(),  # Added here
	GPT4O(),
	# ... rest of models
]
```

### In `model_configuration.py`:

```python
class VisionAIConfigurationPanel(BaseModelSettingsPanel):
	model = description_service.VisionAI()
	title = model.name
	
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.add_about_button(sHelper)
		self.add_api_key_field(sHelper)
		self.add_prompt_field(sHelper)
		self.add_max_tokens_field(sHelper)
		self.add_timeout_field(sHelper)
		super().makeSettings(settingsSizer)

# Assign the panel
description_service.VisionAI.configurationPanel = VisionAIConfigurationPanel
```

### In `configspec.py`:

```python
[VisionAI Pro]  # Matches the name property exactly
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)
```

## Final notes

The current feature set supports everything needed to start and carry on multi-turn conversations with each of the APIs I've seen to date.
That said, if you've encountered one that doesn't seem to work with this system, open an issue and I'll take a look. Suggestions on cleaning this up are also highly appreciated.

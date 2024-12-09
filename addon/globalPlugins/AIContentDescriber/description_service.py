# Vision API interfaces for the AI Content Describer NVDA add-on
# Copyright (C) 2023, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import base64
import json
import os.path
import tempfile
import functools
import urllib.parse
import urllib.request
import logHandler
log = logHandler.log

import addonHandler
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Couldn't initialise translations. Is this addon running from NVDA's scratchpad directory?")

import config_handler as ch
import cache


def encode_image(image_path):
	with open(image_path, "rb") as image_file:
		return base64.b64encode(image_file.read()).decode('utf-8')


def get(*args, **kwargs):
	"""Get the contents of a URL and report status information back to NVDA.
	Arguments are the same as those accepted by urllib.request.urlopen.
	"""
	import ui
	import tones
	#translators: error
	error=_("error")
	try:
		response=urllib.request.urlopen(*args, **kwargs).read()
	except IOError as i:
		tones.beep(150, 200)
		#translators: message spoken when we can't connect (error with connection)
		error_connection=_("error making connection")
		if str(i).find("Errno 11001")>-1:
			ui.message(error_connection)
		elif str(i).find("Errno 10060")>-1:
			ui.message(error_connection)
		elif str(i).find("Errno 10061")>-1:
			#translators: message spoken when the connection is refused by our target
			ui.message(_("error, connection refused by target"))
		else:
			reason = str(i)
			if hasattr(i, "fp"):
				error_text = i.fp.read()
				error_text = json.loads(error_text)
				if "error" in error_text:
					reason += ". "+error_text["error"]["message"]
			ui.message(error+": "+reason)
			raise
		return
	except Exception as i:
		tones.beep(150, 200)
		ui.message(error+": "+str(i))
		return
	return response


def post(**kwargs):
	"""Post to a URL and report status information back to NVDA.
	Keyword arguments are the same as those accepted by urllib.request.Request, except for timeout, which is handled separately.
	"""
	import ui
	import tones
	#translators: error
	error=_("error")
	kwargs["method"] = "POST"
	if "timeout" in kwargs:
		timeout = kwargs.get("timeout", 10)
		del kwargs["timeout"]
	else:
		timeout = 10
	try:
		request = urllib.request.Request(**kwargs)
		response=urllib.request.urlopen(request, timeout=timeout).read()
	except IOError as i:
		tones.beep(150, 200)
		#translators: message spoken when we can't connect (error with connection)
		error_connection=_("error making connection")
		if str(i).find("Errno 11001")>-1:
			ui.message(error_connection)
		elif str(i).find("Errno 10060")>-1:
			ui.message(error_connection)
		elif str(i).find("Errno 10061")>-1:
			#translators: message spoken when the connection is refused by our target
			ui.message(_("error, connection refused by target"))
		else:
			reason = str(i)
			if hasattr(i, "fp"):
				error_text = i.fp.read()
				print(error_text)
				error_text = json.loads(error_text)
				if "error" in error_text:
					reason += ". "+error_text["error"]["message"]
			ui.message(error+": "+reason)
			raise
		return
	except Exception as i:
		tones.beep(150, 200)
		ui.message(error+": "+str(i))
		return
	return response


class BaseDescriptionService:
	name = "unknown"
	DEFAULT_PROMPT = "Describe this image succinctly, but in as much detail as possible to someone who is blind. If there is text, ensure it is included in your response."
	supported_formats = []
	description = "Another vision capable large language model"
	about_url = ""
	needs_api_key = True
	needs_base_url = False
	needs_configuration_dialog = True
	configurationPanel = None

	@property
	def api_key(self):
		return ch.config[self.name]["api_key"]

	@api_key.setter
	def api_key(self, key):
		ch.config[self.name]["api_key"] = key

	@property
	def base_url(self):
		return ch.config[self.name]["base_url"]

	@base_url.setter
	def base_url(self, value):
		ch.config[self.name]["base_url"] = value

	@property
	def chosen_model(self):
		"""When a provider supports more than one model, like Ollama, this is the last one that was selected."""
		return ch.config[self.name]["chosen_model"]

	@chosen_model.setter
	def chosen_model(self, value):
		ch.config[self.name]["chosen_model"] = value

	@property
	def max_tokens(self):
		return ch.config[self.name]["max_tokens"]

	@max_tokens.setter
	def max_tokens(self, value):
		ch.config[self.name]["max_tokens"] = value

	@property
	def prompt(self):
		return ch.config[self.name]["prompt"] or self.DEFAULT_PROMPT

	@prompt.setter
	def prompt(self, value):
		ch.config[self.name]["prompt"] = value

	@property
	def timeout(self):
		return ch.config[self.name]["timeout"]

	@timeout.setter
	def timeout(self, value):
		ch.config[self.name]["timeout"] = value

	@property
	def is_available(self):
		if not self.needs_api_key and not self.needs_base_url:
			return True
		if (self.needs_api_key and self.api_key) or (self.needs_base_url and self.base_url):
			return True
		return False

	def __str__(self):
		return f"{self.name}: {self.description}"

	def save_config(self):
		ch.config.write()

	def process(self):
		pass  # implement in subclasses


def cached_description(func):
	"""
	Wraps a description service to provide caching of descriptions. That way, if the same image is 
	processed multiple times, the description is only fetched once from the API. 

	Usage (In a child of `BaseDescription`):
	```py
	@cached_description
	def process(self, image_path, *args, **kwargs):
		# your processing logic here
		# Safely omit anything having to do with caching, as this function does that for you.
		# note, however, that if there is an image in the cache, your function will never be called.
		return description
	```
	"""
	# TODO: remove fallback cache in later versions
	FALLBACK_CACHE_NAME = "images"
	@functools.wraps(func)
	def wrapper(self, image_path, *args, **kw):
		is_cache_enabled = kw.get("cache_descriptions", True)
		base64_image = encode_image(image_path)
		# (optionally) read the cache
		if is_cache_enabled:
			cache.read_cache(self.name)
			description = cache.cache[self.name].get(base64_image)
			if description is None:
				# TODO: remove fallback cache in later versions
				cache.read_cache(FALLBACK_CACHE_NAME)
				description = cache.cache[FALLBACK_CACHE_NAME].get(base64_image)
			if description is not None:
				log.debug(f"Cache hit. Using cached description for {image_path} from {self.name}")
				return description
		# delegate to the wrapped description service
		log.debug(f"Cache miss. Fetching description for {image_path} from {self.name}")
		description = func(self, image_path, **kw)
		# (optionally) update the cache
		if is_cache_enabled:
			cache.read_cache(self.name)
			cache.cache[self.name][base64_image] = description
			cache.write_cache(self.name)
		
		return description
	return wrapper



class BaseGPT(BaseDescriptionService):
	supported_formats = [
		".gif",
		".jpeg",
		".jpg",
		".png",
		".webp",
	]
	needs_api_key = True

	def __init__(self):
		super().__init__()

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {self.api_key}"
		}
		payload = {
			"model": self.internal_model_name,
			"messages": [
				{
					"role": "user",
					"content": [
						{
							"type": "text",
							"text": self.prompt
						},
						{
							"type": "image_url",
							"image_url": {
								"url": f"data:image/jpeg;base64,{base64_image}"
							}
						}
					]
				}
			],
			"max_tokens": self.max_tokens
		}
		response = post(url="https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response = json.loads(response.decode('utf-8'))
		content = response["choices"][0]["message"]["content"]
		if not content:
			ui.message("content returned none")
		if content:
			return content


class GPT4(BaseGPT):
	name = "GPT-4 vision"
	# translators: the description for the GPT4 vision model in the model configuration dialog
	description = _("The GPT4 model from OpenAI, previewed with vision capabilities. As of April 2024,  this model has been superseded by GPT4 turbo which has consistently achieved better metrics in tasks involving visual understanding.")
	about_url = "https://platform.openai.com/docs/guides/vision"
	internal_model_name = "gpt-4-vision-preview"


class GPT4Turbo(BaseGPT):
	name = "GPT-4 turbo"
	# translators: the description for the GPT4 turbo model in the model configuration dialog
	description = _("The next generation of the original GPT4 vision preview, with enhanced quality and understanding.")
	about_url = "https://help.openai.com/en/articles/8555510-gpt-4-turbo-in-the-openai-api"
	internal_model_name = "gpt-4-turbo"


class GPT4O(BaseGPT):
	name = "GPT-4 omni"
	# translators: the description for the GPT4 omni model in the model configuration dialog
	description = _("OpenAI's first fully multimodal model, released in May 2024. This model has the same high intelligence as GPT4 and GPT4 turbo, but is much more efficient, able to generate text at twice the speed and at half the cost.")
	about_url = "https://openai.com/index/hello-gpt-4o/"
	internal_model_name = "gpt-4o"


class GoogleGemini(BaseDescriptionService):
	supported_formats = [
		".jpeg",
		".jpg",
		".png",
	]
	needs_api_key = True

	def __init__(self):
		super().__init__()

	@cached_description
	def process(self, image_path, **kw):
		# Don't call this function directly
		base64_image = encode_image(image_path)
		headers = {
			"Content-Type": "application/json"
		}
		payload = {"contents":[
			{
				"parts":[
					{"text": self.prompt},
					{
						"inline_data": {
							"mime_type":"image/jpeg",
							"data": base64_image
						}
					}
				]
			}],
			"generationConfig": {
				"maxOutputTokens": self.max_tokens
			}
		}
		response = post(url=f"https://generativelanguage.googleapis.com/v1beta/models/{self.internal_model_name}:generateContent?key={self.api_key}", headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response = json.loads(response.decode('utf-8'))
		if "error" in response:
			#translators: message spoken when Google gemini encounters an error with the format or content of the input.
			ui.message(_("Gemini encountered an error: {code}, {msg}").format(code=response['error']['code'], msg=response['error']['message']))
			return
		return response["candidates"][0]["content"]["parts"][0]["text"]

class Gemini(GoogleGemini):
	name = "Google Gemini pro vision"
	internal_model_name = "gemini-1.5-flash"
	# translators: the description for the Google Gemini pro vision model in the model configuration dialog
	description = _("Google's Gemini 1.5 flash model with vision capabilities.")
	about_url = "https://blog.google/technology/ai/google-gemini-update-flash-ai-assistant-io-2024/#gemini-model-updates"

class GeminiFlash1_5_8B(GoogleGemini):
	name = "Google Gemini 1.5 Flash-8B"
	internal_model_name = "gemini-1.5-flash-8b"
	# translators: the description for Google's Gemini 1.5 Flash-8B model, as shown in the configuration dialog.
	description = _("Gemini 1.5 Flash-8B is a small model designed for high volume and lower intelligence tasks.")
	about_url = "https://developers.googleblog.com/en/gemini-15-flash-8b-is-now-generally-available-for-use/"

class Gemini1_5Pro(GoogleGemini):
	name = "Google Gemini 1.5 Pro"
	internal_model_name = "gemini-1.5-pro"
	# translators: the description for Google's Gemini 1.5 pro model, as shown in the configuration dialog.
	description = _("Gemini 1.5 Pro is a mid-size multimodal model that is optimized for a wide-range of complex reasoning tasks requiring more intelligence. 1.5 Pro can process large amounts of data at once.")
	about_url = "https://deepmind.google/technologies/gemini/pro/"

class Anthropic(BaseDescriptionService):
	supported_formats = [
		".jpeg",
		".jpg",
		".png",
		".gif",
		".webp"
	]

	@cached_description
	def process(self, image_path, **kw):
		# Do not use this function directly, override it in subclasses and call with the model parameter
		base64_image = encode_image(image_path)
		mimetype = os.path.splitext(image_path)[1].lower()
		if not mimetype in self.supported_formats:
			# try falling back to png
			mimetype = ".png"
		mimetype = mimetype[1:]  # trim the "."
		headers = {
			"User-Agent": "curl/8.4.0",  # Cloudflare is perplexingly blocking anything that urllib sends with an "error 1010"
			"Content-Type": "application/json",
			"x-api-key": self.api_key,
			"anthropic-version": "2023-06-01"
		}
		payload = {
			"model": self.internal_model_name,
			"messages": [
				{"role": "user", "content": [
					{
						"type": "image",
						"source": {
							"type": "base64",
							"media_type": "image/"+mimetype,
							"data": base64_image,
						}
					},
					{
						"type": "text",
						"text": self.prompt
					}
				]}
			],
			"max_tokens": self.max_tokens
		}
		response = post(url="https://api.anthropic.com/v1/messages", headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response = json.loads(response.decode('utf-8'))
		if response["type"] == "error":
			#translators: message spoken when Claude encounters an error with the format or content of the input.
			ui.message(_("Claude encountered an error. {err}").format(err=response['error']['message']))
			return
		return response["content"][0]["text"]


class Claude3_5Sonnet(Anthropic):
	name = "Claude 3.5 Sonnet"
	description = _("Anthropic's improvement over Claude 3 sonnet, this model features enhanced reasoning capabilities relative to its predecessor.")
	internal_model_name = "claude-3-5-sonnet-20240620"


class Claude3Opus(Anthropic):
	name = "Claude 3 Opus"
	description = _("Anthropic's most powerful model for highly complex tasks.")
	internal_model_name = "claude-3-opus-20240229"


class Claude3Sonnet(Anthropic):
	name = "Claude 3 Sonnet"
	description = _("Anthropic's model with Ideal balance of intelligence and speed, excels for enterprise workloads.")
	internal_model_name = "claude-3-sonnet-20240229"


class Claude3Haiku(Anthropic):
	name = "Claude 3 Haiku"
	description = _("Anthropic's fastest and most compact model for near-instant responsiveness")
	internal_model_name = "claude-3-haiku-20240307"


class MistralAI(BaseDescriptionService):
	supported_formats = [
		".png",
		".jpg",
		".jpeg",
		".webp",
		".gif"
	]
	needs_api_key = True

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		mimetype = os.path.splitext(image_path)[1].lower()
		if not mimetype in self.supported_formats:
			# try falling back to png
			mimetype = ".png"
		mimetype = mimetype[1:]  # trim the "."
		headers = {
			"User-Agent": "curl/8.4.0",  # to shut up CloudFlare
			"Content-Type": "application/json",
			"Authorization": "Bearer "+self.api_key
		}
		payload = {
			"model": self.internal_model_name,
			"messages": [
				{
					"role": "user",
					"content": [
						{"type": "text", "text": self.prompt},
						{"type": "image_url", "image_url": f"data:image/{mimetype};base64,{base64_image}"}
					]
				}
			],
			"max_tokens": self.max_tokens
		}
		response = post(url="https://api.mistral.ai/v1/chat/completions", headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response = json.loads(response.decode('utf-8'))
		content = response["choices"][0]["message"]["content"]
		if not content:
			ui.message("content returned none")
		if content:
			return content


class PixtralLarge(MistralAI):
	name = "Pixtral Large"
	# translators: the description for MistralAI's Pixtral Large model, as shown in the configuration dialog.
	description = _("MistralAI's multimodal image LLM, achieving state-of-the-art results on MathVista, DocVQA, VQAv2 and other benchmarks.")
	internal_model_name = "pixtral-large-latest"
	about_url = "https://mistral.ai/news/pixtral-large/"


class Ollama(BaseDescriptionService):
	name = "Ollama"
	needs_api_key = False
	needs_base_url = True
	# translators: the description for the Ollama model, as shown in the configuration dialog
	description = _("The quickest way to get up and running with large language models.")
	supported_formats = [
		".jpeg",
		".jpg",
		".png",
	]
	about_url = "https://github.com/ollama/ollama/blob/main/README.md#quickstart"

	def list_model_names(self, base_url):
		base_url = base_url or self.base_url
		url = urllib.parse.urljoin(base_url, "api/tags")
		try:
			content = urllib.request.urlopen(url=url).read()
		except Exception as exc:
			import ui
			# translators: the message spoken in the Ollama configuration dialog upon pressing "list models", when the base URL cannot be contacted.
			ui.message(_("Could not contact the provided base URL. "+str(exc)))
			return
		content = json.loads(content)
		models = [model["model"] for model in content["models"]]
		return models

	@cached_description
	def process(self, image_path, **kw):
		model_name = kw.get("chosen_model") or self.chosen_model
		url = kw.get("base_url") or self.base_url
		url = urllib.parse.urljoin(url, "api/chat")
		base64_image = encode_image(image_path)
		headers = {
			"Content-Type": "application/json"
		}
		payload = {
			"model": model_name,
			"messages": [
				{
					"role": "user",
					"content": self.prompt,
					"images": [base64_image]
				}
			],
			"stream": False
		}
		response = post(url=url, headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response = json.loads(response.decode('utf-8'))
		if not "message" in response:
			ui.message(_("The response appears to be malformed. "+repr(response)))
			return
		return response["message"]["content"]\


class LlamaCPP(BaseDescriptionService):
	name = "llama.cpp"
	needs_api_key = False
	needs_base_url = True
	supported_formats = [
		".jpeg",
		".jpg",
		".png",
	]
	# translators: the description for the llama.cpp option in the model configuration dialog
	description = _("""llama.cpp is a state-of-the-art, open-source solution for running large language models locally and in the cloud.
This add-on integration assumes that you have obtained llama.cpp from Github and an image capable model from Huggingface or another repository, and that a server is currently running to handle requests. Though the process for getting this working is largely a task for the user that knows what they are doing, you can find basic steps in the add-on documentation.""")

	@cached_description
	def process(self, image_path, **kw):
		url = kw.get("base_url", "http://localhost:8080")
		url = urllib.parse.urljoin(url, "completion")
		base64_image = encode_image(image_path)
		headers = {
			"Content-Type": "application/json"
		}
		payload = {
			"prompt": f"USER: [img-12]\n{self.prompt}ASSISTANT:",
			"stream": False,
			"image_data": [{
				"data": base64_image,
				"id": 12
			}],
			"temperature": 1.0,
			"n_predict": self.max_tokens
		}
		response = post(url=url, headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response = json.loads(response.decode('utf-8'))
		if not "content" in response:
			ui.message(_("Image recognition response appears to be malformed.\n{response}").format(response=repr(response)))
		return response["content"]


models = [
	GPT4O(),
	GPT4Turbo(),
	GPT4(),
	Claude3_5Sonnet(),
	Claude3Haiku(),
	Claude3Opus(),
	Claude3Sonnet(),
	Gemini(),
	GeminiFlash1_5_8B(),
	Gemini1_5Pro(),
	PixtralLarge(),
	Ollama(),
	LlamaCPP(),
]


def list_available_models():
	return [model for model in models if model.is_available]


def list_available_model_names():
	return [model.name for model in list_available_models()]


def get_model_by_name(model_name):
	model_name = model_name.lower()
	for model in models:
		if model.name.lower() == model_name:
			return model

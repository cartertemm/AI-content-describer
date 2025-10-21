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
import hashlib
import uuid 
import vivo_auth
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


def get_image_hash(image_path):
	"""Generate a consistent hash for an image file to use as conversation key"""
	with open(image_path, "rb") as f:
		return hashlib.md5(f.read()).hexdigest()


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
	DEFAULT_PROMPT = "Describe this image succinctly, but in as much detail as possible. If there is text, ensure it is included in your response exactly as shown."
	supported_formats = []
	description = "Another vision capable large language model"
	about_url = ""
	needs_api_key = True
	needs_base_url = False
	needs_configuration_dialog = True
	configurationPanel = None

	# Conversation management
	_active_conversation = None
	_conversations = {}  # image_hash: messages list

	@property
	def api_key(self):
		return ch.config[self.name].get("api_key")

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

	def build_conversation_payload(self, messages, **kw):
		"""
		Convert a list of messages into the format this provider expects.
		The format of the messages parameter is:
		[
			{"role": "user", "content": "describe this image", "image": base64_data},
			{"role": "assistant", "content": "I see a cat..."},
			{"role": "user", "content": "what color is the cat?"},
		]
		This default implementation works for OpenAI-compatible APIs.
		You will need to override this method in child classes for providers with different formats.
		"""
		formatted_messages = []
		for msg in messages:
			if msg["role"] == "user" and msg.get("image"):
				# This is a user message with an image attached
				formatted_msg = {
					"role": "user",
					"content": [
						{"type": "text", "text": msg["content"]},
						{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{msg['image']}"}}
					]
				}
			else:
				# a text-only message
				formatted_msg = {
					"role": msg["role"],
					"content": msg["content"]
				}
			formatted_messages.append(formatted_msg)
		return {
			"model": getattr(self, 'internal_model_name', self.name),
			"messages": formatted_messages,
			"max_tokens": self.max_tokens
		}

	def _get_conversation_headers(self):
		"""Get headers for API requests. Override if needed."""
		headers = {"Content-Type": "application/json"}
		if self.needs_api_key and self.api_key:
			headers["Authorization"] = f"Bearer {self.api_key}"
		return headers

	def _get_conversation_url(self):
		"""Get URL for API requests. Override if needed."""
		return "https://api.openai.com/v1/chat/completions"

	def _extract_conversation_response(self, response_json):
		"""Extract the assistant's response from API response. Override if needed."""
		return response_json["choices"][0]["message"]["content"]

	def start_conversation(self, image_path=None, initial_prompt=None, initial_response=None):
		"""Start a new conversation, optionally with an image"""
		messages = []
		if image_path and initial_prompt and initial_response:
			# We have an image/initial prompt and response i.e. a description
			image_hash = get_image_hash(image_path)
			base64_image = encode_image(image_path)
			messages = [
				{"role": "user", "content": initial_prompt, "image": base64_image},
				{"role": "assistant", "content": initial_response}
			]
			self._conversations[image_hash] = messages
			self._active_conversation = image_hash
		elif initial_prompt and initial_response:
			# Text only
			conversation_id = "text_chat_" + str(len(self._conversations))
			messages = [
				{"role": "user", "content": initial_prompt},
				{"role": "assistant", "content": initial_response}
			]
			self._conversations[conversation_id] = messages
			self._active_conversation = conversation_id
		else:
			# Empty conversation: edge case
			conversation_id = "empty_chat_" + str(len(self._conversations))
			self._conversations[conversation_id] = []
			self._active_conversation = conversation_id

	def add_to_conversation(self, user_message, image_path=None, include_original_image=True):
		"""Add user message and get AI response. Returns the AI's response."""
		if not self._active_conversation or self._active_conversation not in self._conversations:
			raise ValueError("No active conversation. Start one first.")
		messages = self._conversations[self._active_conversation].copy()
		new_message = {"role": "user", "content": user_message}
		if image_path:
			new_message["image"] = encode_image(image_path)
		elif include_original_image and messages:
			for msg in messages:
				if msg["role"] == "user" and msg.get("image"):
					new_message["image"] = msg["image"]
					break
		messages.append(new_message)
		payload = self.build_conversation_payload(messages)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(url=url, headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response_json = json.loads(response.decode('utf-8'))
		ai_response = self._extract_conversation_response(response_json)
		messages.append({"role": "assistant", "content": ai_response})
		self._conversations[self._active_conversation] = messages
		return ai_response

	def has_conversation(self):
		"""Check if there's an active conversation for follow-ups"""
		return (self._active_conversation is not None and 
				self._active_conversation in self._conversations and 
				len(self._conversations[self._active_conversation]) > 0)

	def get_conversation_summary(self):
		"""Get a simple summary of the current conversation (for debugging)"""
		if not self.has_conversation():
			return "No active conversation"
		messages = self._conversations[self._active_conversation]
		return f"Conversation with {len(messages)} messages (last: {messages[-1]['role']})"

	def clear_conversation(self, conversation_id=None):
		"""Clear conversation state"""
		if conversation_id:
			if conversation_id in self._conversations:
				del self._conversations[conversation_id]
			if self._active_conversation == conversation_id:
				self._active_conversation = None
		else:
			self._conversations.clear()
			self._active_conversation = None

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
				# Start a conversation in case the user wishes to follow-up
				self.start_conversation(image_path, self.prompt, description)
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
	openai_url = "https://api.openai.com/v1/chat/completions"

	def _get_conversation_headers(self):
		headers = {
			"Content-Type": "application/json",
			"User-Agent": "curl/8.4.0"
		}
		if self.needs_api_key:
			headers["Authorization"] = f"Bearer {self.api_key}"
		return headers

	def _get_conversation_url(self):
		return getattr(self, 'openai_url', "https://api.openai.com/v1/chat/completions")

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		messages = [{
			"role": "user",
			"content": self.prompt,
			"image": base64_image
		}]
		payload = self.build_conversation_payload(messages)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(url=url, headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response_json = json.loads(response.decode('utf-8'))
		content = self._extract_conversation_response(response_json)
		if not content:
			import ui
			ui.message("content returned none")
			return
		self.start_conversation(image_path, self.prompt, content)
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
	description = _("The next generation of the original GPT4 vision preview, with enhanced quality and understanding. This model will soon be deprecated so we recommend switching to GPT-4o.")
	about_url = "https://help.openai.com/en/articles/8555510-gpt-4-turbo-in-the-openai-api"
	internal_model_name = "gpt-4-turbo"


class GPT4O(BaseGPT):
	name = "GPT-4 omni"
	# translators: the description for the GPT4 omni model in the model configuration dialog
	description = _("OpenAI's first fully multimodal model, released in May 2024. This model has the same high intelligence as GPT4 and GPT4 turbo, but is much more efficient, able to generate text at twice the speed and at half the cost.")
	about_url = "https://openai.com/index/hello-gpt-4o/"
	internal_model_name = "gpt-4o"

class GPT5Chat(BaseGPT):
	name = "GPT-5 chat"
	# translators: the description for the GPT‑5 chat model in the configuration dialog
	description = _("GPT-5 model used in ChatGPT")
	about_url = "https://platform.openai.com/docs/models/gpt-5-chat-latest"
	internal_model_name = "gpt-5-chat-latest"


class O3(BaseGPT):
	name = "OpenAI O3"
	# translators: the description for the OpenAI O3 model in the model configuration dialog
	description = _("Released in April 2025, o3 is a well-rounded and powerful model across domains. It sets a new standard for math, science, coding, and visual reasoning tasks. It also excels at technical writing and instruction-following. Use it to think through multi-step problems that involve analysis across text, code, and images.")
	about_url = "https://openai.com/index/introducing-o3-and-o4-mini/"
	internal_model_name = "o3"


class O3Pro(BaseGPT):
	name = "OpenAI O3 pro"
	# translators: the description for the OpenAI O3 pro model in the model configuration dialog
	description = _("Released in June 2025, O3 pro is an upgraded version of O3. It is designed to think longer and provide the most reliable responses. Because o3-pro has access to tools, responses typically take longer than o1-pro to complete. We recommend using it for challenging questions where reliability matters more than speed, and waiting a few minutes is worth the tradeoff. Do not forget to tweak the timeout setting.")
	about_url = "https://help.openai.com/en/articles/9624314-model-release-notes"
	internal_model_name = "o3-pro"


class O3Mini(BaseGPT):
	name = "OpenAI O3 mini"
	# translators: the description for the OpenAI O3 mini model in the model configuration dialog
	description = _("Released in January 2025, this powerful and fast model advances the boundaries of what small models can achieve, delivering exceptional STEM capabilities with particular strength in science, math, and coding all while maintaining the low cost and reduced latency of OpenAI o1-mini.")
	about_url = "https://openai.com/index/openai-o3-mini/"
	internal_model_name = "o3-mini"


class O4Mini(BaseGPT):
	name = "OpenAI O4 mini"
	# translators: the description for the OpenAI O4 mini model in the model configuration dialog
	description = _("Released in April 2025, o4-mini is a smaller model optimized for fast, cost-efficient reasoning. It achieves remarkable performance for its size and cost, particularly in math, coding, and visual tasks. It has been shown to outperform O3 mini and supports significantly higher usage limits than o3, making it a strong high-volume, high-throughput option for questions that benefit from reasoning. Do not forget to tweak the timeout setting.")
	about_url = "https://openai.com/index/introducing-o3-and-o4-mini/"
	internal_model_name = "o4-mini"


class PollinationsAI(BaseGPT):
	name = "Pollinations (OpenAI)"
	# translators: The description for the PollinationsAI model with OpenAI support in the model selection dialog.
	description = "Pollinations.AI is an open-source gen AI startup based in Berlin, providing the most easy-to-use, free text and image generation API available. It integrates with state-of-the-art models, no signups or API keys required."
	needs_api_key = False
	openai_url = "https://text.pollinations.ai/openai"
	internal_model_name = "openai"


class GoogleGemini(BaseDescriptionService):
	supported_formats = [
		".jpeg",
		".jpg",
		".png",
	]
	needs_api_key = True

	def build_conversation_payload(self, messages, **kw):
		"""Override for Gemini's contents/parts format"""
		contents = []
		for msg in messages:
			parts = [{"text": msg["content"]}]
			if msg.get("image"):
				parts.insert(0, {
					"inline_data": {
						"mime_type": "image/jpeg",
						"data": msg["image"]
					}
				})
			role = msg["role"]
			if role == "assistant":
				role = "model"  # Google refers to the assistant role as "model"
			contents.append({"role": role, "parts": parts})
		return {
			"contents": contents,
			"generationConfig": {
				"maxOutputTokens": self.max_tokens
			}
		}

	def _get_conversation_url(self):
		return f"https://generativelanguage.googleapis.com/v1beta/models/{self.internal_model_name}:generateContent?key={self.api_key}"

	def _get_conversation_headers(self):
		return {"Content-Type": "application/json"}

	def _extract_conversation_response(self, response_json):
		if "error" in response_json:
			import ui
			#translators: message spoken when Google gemini encounters an error with the format or content of the input.
			ui.message(_("Gemini encountered an error: {code}, {msg}").format(code=response_json['error']['code'], msg=response_json['error']['message']))
			return ""
		return response_json["candidates"][0]["content"]["parts"][0]["text"]

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		messages = [{
			"role": "user",
			"content": self.prompt,
			"image": base64_image
		}]
		payload = self.build_conversation_payload(messages)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(url=url, headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response_json = json.loads(response.decode('utf-8'))
		content = self._extract_conversation_response(response_json)
		if not content:
			return
		self.start_conversation(image_path, self.prompt, content)
		return content

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


class Gemini2_5FlashPreview(GoogleGemini):
	name = "Google Gemini 2.5 Flash Preview"
	internal_model_name = "gemini-2.5-flash-preview-05-20"
	# translators: the description for Google's Gemini 2.5 Flash Preview model, as shown in the configuration dialog.
	description = _("Gemini 2.5 Flash delivers fast performance for complex tasks. Ideal for tasks like summarization, chat applications, data extraction, and captioning.")
	about_url = "https://deepmind.google/models/gemini/flash/"


class Gemini2_5ProPreview(GoogleGemini):
	name = "Google Gemini 2.5 Pro Preview"
	internal_model_name = "gemini-2.5-pro-preview-06-05"
	# translators: the description for Google's Gemini 2.5 Pro Preview model, as shown in the configuration dialog.
	description = _("Gemini 2.5 Pro models are capable of reasoning through their thoughts before responding, resulting in enhanced performance and improved accuracy. Best for coding and complex tasks.")
	about_url = "https://deepmind.google/models/gemini/pro/"


class Gemini2_0Flash(GoogleGemini):
	name = "Google Gemini 2.0 Flash"
	internal_model_name = "gemini-2.0-flash-001"
	# translators: the description for Google's Gemini 2.0 Flash model, as shown in the configuration dialog.
	description = _("Gemini 2.0 Flash delivers next-gen features and improved capabilities, including superior speed, native tool use, multimodal generation, and a 1M token context window.")
	about_url = "https://deepmind.google/technologies/gemini/flash/"


class Gemini2_0FlashLitePreview(GoogleGemini):
	name = "Google Gemini 2.0 Flash-Lite Preview"
	internal_model_name = "gemini-2.0-flash-lite-preview-02-05"
	# translators: the description for Google's Gemini 2.0 Flash model, as shown in the configuration dialog.
	description = _("Gemini 2.0 Flash lite preview is a Gemini 2.0 Flash model optimized for cost efficiency and low latency. Outperforms 1.5 Flash on the majority of benchmarks, at the same speed and cost.")
	about_url = "https://deepmind.google/technologies/gemini/flash-lite/"


class Anthropic(BaseDescriptionService):
	supported_formats = [
		".jpeg",
		".jpg",
		".png",
		".gif",
		".webp"
	]

	def build_conversation_payload(self, messages, **kw):
		"""Override for Anthropic's message format with content arrays"""
		formatted_messages = []
		for msg in messages:
			content = [{"type": "text", "text": msg["content"]}]
			if msg.get("image"):
				content.insert(0, {
					"type": "image",
					"source": {
						"type": "base64",
						"media_type": "image/png",
						"data": msg["image"]
					}
				})
			formatted_messages.append({"role": msg["role"], "content": content})
		return {
			"model": self.internal_model_name,
			"messages": formatted_messages,
			"max_tokens": self.max_tokens
		}

	def _get_conversation_url(self):
		return "https://api.anthropic.com/v1/messages"

	def _get_conversation_headers(self):
		return {
			"User-Agent": "curl/8.4.0",
			"Content-Type": "application/json",
			"x-api-key": self.api_key,
			"anthropic-version": "2023-06-01"
		}

	def _extract_conversation_response(self, response_json):
		if response_json.get("type") == "error":
			import ui
			#translators: message spoken when Claude encounters an error with the format or content of the input.
			ui.message(_("Claude encountered an error. {err}").format(err=response_json['error']['message']))
			return ""
		return response_json["content"][0]["text"]

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		messages = [{
			"role": "user",
			"content": self.prompt,
			"image": base64_image
		}]
		payload = self.build_conversation_payload(messages)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(url=url, headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response_json = json.loads(response.decode('utf-8'))
		content = self._extract_conversation_response(response_json)
		if not content:
			return
		self.start_conversation(image_path, self.prompt, content)
		return content


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


class Claude3_5Sonnet(Anthropic):
	name = "Claude 3.5 Sonnet"
	description = _("Anthropic's improvement over Claude 3 sonnet, this model features enhanced reasoning capabilities relative to its predecessor.")
	internal_model_name = "claude-3-5-sonnet-20240620"


class Claude3_5Haiku(Anthropic):
	name = "Claude 3.5 Haiku"
	# translators: the description for the Claude 3.5 Haiku model in the model configuration dialog
	description = _("Anthropic's next generation fastest model with improved reasoning across every skill set. Surpasses Claude 3 Opus on many benchmarks while maintaining speed and cost-effectiveness.")
	about_url = "https://www.anthropic.com/claude/haiku"
	internal_model_name = "claude-3-5-haiku-20241022"


class Claude3_5SonnetV2(Anthropic):
	name = "Claude 3.5 Sonnet v2"
	# translators: the description for the Claude 3.5 Sonnet v2 model in the model configuration dialog
	description = _("Anthropic's upgraded Claude 3.5 Sonnet with significant improvements in coding and computer use capabilities. Features enhanced reasoning and the ability to interact with computer interfaces.")
	about_url = "https://www.anthropic.com/news/3-5-models-and-computer-use"
	internal_model_name = "claude-3-5-sonnet-20241022"


class Claude3_7Sonnet(Anthropic):
	name = "Claude 3.7 Sonnet"
	# translators: the description for the Claude 3.7 Sonnet model in the model configuration dialog
	description = _("Anthropic's most intelligent model to date and the first hybrid reasoning model. Features extended thinking capabilities for complex problem-solving with step-by-step reasoning.")
	about_url = "https://docs.anthropic.com/en/docs/about-claude/models"
	internal_model_name = "claude-3-7-sonnet-20250219"


class Claude4Sonnet(Anthropic):
	name = "Claude 4 Sonnet"
	# translators: the description for the Claude 4 Sonnet model in the model configuration dialog
	description = _("Anthropic's high-performance model with exceptional reasoning and efficiency. Significant upgrade to Claude Sonnet 3.7 with superior coding and enhanced instruction following.")
	about_url = "https://www.anthropic.com/claude/sonnet"
	internal_model_name = "claude-sonnet-4-20250514"


class Claude4Opus(Anthropic):
	name = "Claude 4 Opus"
	# translators: the description for the Claude 4 Opus model in the model configuration dialog
	description = _("Anthropic's most capable and intelligent model yet. Sets new standards in complex reasoning and advanced coding with sustained performance on long-running tasks requiring focused effort.")
	about_url = "https://www.anthropic.com/claude/opus"
	internal_model_name = "claude-opus-4-20250514"


class MistralAI(BaseDescriptionService):
	supported_formats = [
		".png",
		".jpg",
		".jpeg",
		".webp",
		".gif"
	]
	needs_api_key = True

	def _get_conversation_url(self):
		return "https://api.mistral.ai/v1/chat/completions"

	def _get_conversation_headers(self):
		return {
			"User-Agent": "curl/8.4.0",
			"Content-Type": "application/json",
			"Authorization": "Bearer " + self.api_key
		}

	def build_conversation_payload(self, messages, **kw):
		"""Override for MistralAI's OpenAI-compatible format with image_url"""
		formatted_messages = []
		for msg in messages:
			if msg["role"] == "user" and msg.get("image"):
				# Message with an image
				formatted_msg = {
					"role": "user",
					"content": [
						{"type": "text", "text": msg["content"]},
						{"type": "image_url", "image_url": f"data:image/jpeg;base64,{msg['image']}"}
					]
				}
			else:
				# Text-only message
				formatted_msg = {
					"role": msg["role"],
					"content": msg["content"]
				}
			formatted_messages.append(formatted_msg)
		return {
			"model": self.internal_model_name,
			"messages": formatted_messages,
			"max_tokens": self.max_tokens
		}

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		messages = [{
			"role": "user",
			"content": self.prompt,
			"image": base64_image
		}]
		payload = self.build_conversation_payload(messages)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(url=url, headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response_json = json.loads(response.decode('utf-8'))
		content = self._extract_conversation_response(response_json)
		if not content:
			import ui
			ui.message("content returned none")
			return
		self.start_conversation(image_path, self.prompt, content)
		return content


class PixtralLarge(MistralAI):
	name = "Pixtral Large"
	# translators: the description for MistralAI's Pixtral Large model, as shown in the configuration dialog.
	description = _("MistralAI's multimodal image LLM, achieving state-of-the-art results on MathVista, DocVQA, VQAv2 and other benchmarks.")
	internal_model_name = "pixtral-large-latest"
	about_url = "https://mistral.ai/news/pixtral-large/"


class Grok2Vision(BaseGPT):
	name = "Grok 2 vision"
	# translators: the description for the xAI Grok 2 model in the model configuration dialog
	description = _("xAI's flagship multimodal model with advanced reasoning capabilities. Excels at enterprise tasks like data extraction, programming, and text summarization with superior domain knowledge in finance, healthcare, law, and science.")
	about_url = "https://x.ai/news/grok-2"
	internal_model_name = "grok-2-vision-latest"
	openai_url = "https://api.x.ai/v1/chat/completions"
	supported_formats = [
		".gif",
		".jpeg",
		".jpg",
		".png",
		".webp",
	]


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

	def build_conversation_payload(self, messages, **kw):
		"""Override for Ollama's chat format with images array"""
		formatted_messages = []
		for msg in messages:
			formatted_msg = {
				"role": msg["role"],
				"content": msg["content"]
			}
			if msg.get("image"):
				formatted_msg["images"] = [msg["image"]]
			formatted_messages.append(formatted_msg)
		return {
			"model": self.chosen_model,
			"messages": formatted_messages,
			"stream": False
		}

	def _get_conversation_url(self):
		return urllib.parse.urljoin(self.base_url, "api/chat")

	def _get_conversation_headers(self):
		return {"Content-Type": "application/json"}

	def _extract_conversation_response(self, response_json):
		if not "message" in response_json:
			import ui
			ui.message(_("The response appears to be malformed. "+repr(response_json)))
			return ""
		return response_json["message"]["content"]

	@cached_description
	def process(self, image_path, **kw):
		# Build single-image conversation
		base64_image = encode_image(image_path)
		messages = [{
			"role": "user",
			"content": self.prompt,
			"image": base64_image
		}]
		# Use conversation methods for consistency
		payload = self.build_conversation_payload(messages)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(url=url, headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response_json = json.loads(response.decode('utf-8'))
		content = self._extract_conversation_response(response_json)
		if not content:
			return
		self.start_conversation(image_path, self.prompt, content)
		return content


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

	def build_conversation_payload(self, messages, **kw):
		"""Override for llama.cpp's completion format with image_data"""
		# Build conversation context as a single prompt
		prompt_parts = []
		image_data = []
		image_id = 1
		for msg in messages:
			if msg["role"] == "user":
				if msg.get("image"):
					prompt_parts.append(f"USER: [img-{image_id}]\n{msg['content']}")
					image_data.append({"data": msg["image"], "id": image_id})
					image_id += 1
				else:
					prompt_parts.append(f"USER: {msg['content']}")
			else:
				prompt_parts.append(f"ASSISTANT: {msg['content']}")
		prompt_parts.append("ASSISTANT:")
		payload = {
			"prompt": "\n".join(prompt_parts),
			"stream": False,
			"temperature": 1.0,
			"n_predict": self.max_tokens
		}
		if image_data:
			payload["image_data"] = image_data
		return payload

	def _get_conversation_url(self):
		return urllib.parse.urljoin(self.base_url or "http://localhost:8080", "completion")

	def _get_conversation_headers(self):
		return {"Content-Type": "application/json"}

	def _extract_conversation_response(self, response_json):
		if not "content" in response_json:
			import ui
			ui.message(_("Image recognition response appears to be malformed.\n{response}").format(response=repr(response_json)))
			return ""
		return response_json["content"]

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		messages = [{
			"role": "user",
			"content": self.prompt,
			"image": base64_image
		}]
		payload = self.build_conversation_payload(messages)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(url=url, headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
		response_json = json.loads(response.decode('utf-8'))
		content = self._extract_conversation_response(response_json)
		if not content:
			return
		self.start_conversation(image_path, self.prompt, content)
		return content


class VivoBlueLMVision(BaseDescriptionService):
	name = "vivo BlueLM Vision (NVDA-CN)"
	description = _("A multimodal model from vivo, accessed via NVDA-CN account. This service is provided by the NVDA Chinese community and requires your nvdacn.com credentials.")
	about_url = "https://nvdacn.com/"
	internal_model_name = "vivo-BlueLM-Vision-Aid"
	needs_api_key = False
	supported_formats = [".jpeg", ".jpg", ".png", ".webp"]

	# Custom properties to manage NVDA-CN credentials from the config file.
	@property
	def nvdacn_user(self):
		return ch.config[self.name].get("nvdacn_user")

	@nvdacn_user.setter
	def nvdacn_user(self, value):
		ch.config[self.name]["nvdacn_user"] = value

	@property
	def nvdacn_pass(self):
		return ch.config[self.name].get("nvdacn_pass")

	@nvdacn_pass.setter
	def nvdacn_pass(self, value):
		ch.config[self.name]["nvdacn_pass"] = value

	@property
	def is_available(self):
		"""Determines if the service is ready based on the presence of both user credentials."""
		return bool(self.nvdacn_user and self.nvdacn_pass)

	def build_conversation_payload(self, messages, **kw):
		"""
		Translates the addon's internal message format to the specific format required by the VIVO API.
		The VIVO API requires image and text to be sent as separate, consecutive user messages.
		"""
		vivo_messages = []
		for msg in messages:
			if msg["role"] == "user":
				if msg.get("image"):
					vivo_messages.append({
						"role": "user",
						"content": f"data:image/jpeg;base64,{msg['image']}",
						"contentType": "image"
					})
				vivo_messages.append({
					"role": "user",
					"content": msg["content"],
					"contentType": "text"
				})
			else: # Assistant messages are straightforward.
				vivo_messages.append({
					"role": "assistant",
					"content": msg["content"],
					"contentType": "text"
				})
		return {
			'model': self.internal_model_name,
			'sessionId': str(uuid.uuid4()),
			"messages": vivo_messages
		}

	def _extract_conversation_response(self, response_json):
		"""
		Extracts content from a successful response or raises an exception for business errors.
		This approach prevents caching of failed API calls.
		"""
		import ui
		if response_json.get("code") != 0:
			error_msg = response_json.get("msg", "Unknown error from vivo API")
			log.warning(f"VIVO API returned a business error. Code: {response_json.get('code')}, Message: {error_msg}")
			formatted_error = _("API Error: {error}").format(error=error_msg)
			ui.message(formatted_error)
			raise IOError(formatted_error)
		data_obj = response_json.get("data", {})
		content_str = data_obj.get("content")
		if not content_str:
			log.info("VIVO API returned a successful response with empty content.")
			return _("The model returned an empty response.")
		try:
			inner_data = json.loads(content_str)
			if isinstance(inner_data, list) and len(inner_data) > 0 and "text" in inner_data[0]:
				return inner_data[0]["text"]
			return content_str
		except (json.JSONDecodeError, TypeError):
			return content_str

	def _perform_vivo_request(self, messages):
		"""
		A centralized helper to handle the VIVO request lifecycle.
		It catches specific, un-messaged errors to provide feedback,
		while letting already-messaged errors from post() propagate.
		"""
		try:
			request_id = str(uuid.uuid4())
			uri = "/vivogpt/completions"
			params = {'requestId': request_id}
			log.debug(f"Preparing VIVO request with ID: {request_id}")
			# This is the only place that might raise an error without a prior ui.message() call.
			headers = vivo_auth.gen_sign_headers(self.nvdacn_user, self.nvdacn_pass, "POST", uri, params)
			headers['Content-Type'] = 'application/json'
			payload = self.build_conversation_payload(messages)
			full_url = f"https://api-ai.vivo.com.cn{uri}?{urllib.parse.urlencode(params)}"
			log.info(f"Sending request to VIVO API endpoint for request ID: {request_id}")
			# The global post() function handles its own UI messaging for network errors and will raise IOError.
			response_bytes = post(url=full_url, headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=self.timeout)
			if not response_bytes:
				# This case is a safeguard; post() should raise an exception on failure.
				raise IOError(_("Network request failed unexpectedly."))
			response_json = json.loads(response_bytes.decode('utf-8'))
			# This method also handles its own UI messaging and will raise IOError on VIVO business errors.
			return self._extract_conversation_response(response_json)
		except (ValueError, ConnectionError, json.JSONDecodeError) as e:
			# This includes auth errors from vivo_auth, or malformed JSON responses.
			import ui
			log.error(f"An error occurred during VIVO request preparation or parsing: {e}", exc_info=True)
			ui.message(str(e))
			# Re-throw the exception to ensure the operation fails correctly.
			raise

	@cached_description
	def process(self, image_path, **kw):
		"""
		Handles the initial image description request.
		It is wrapped by @cached_description, so any exception thrown will prevent
		the failed result from being cached.
		"""
		messages = [{
			"role": "user",
			"content": self.prompt,
			"image": encode_image(image_path)
		}]
		content = self._perform_vivo_request(messages)
		self.start_conversation(image_path, self.prompt, content)
		return content

	def add_to_conversation(self, user_message, image_path=None, include_original_image=True):
		"""
		Handles follow-up questions in a multimodal conversation.
		"""
		import ui
		if not self.has_conversation():
			error_msg = _("No active conversation. Please describe an image first.")
			ui.message(error_msg)
			return error_msg
		messages = self._conversations[self._active_conversation].copy()
		new_message = {"role": "user", "content": user_message}
		if image_path:
			new_message["image"] = encode_image(image_path)
		messages.append(new_message)
		try:
			ai_response = self._perform_vivo_request(messages)
			messages.append({"role": "assistant", "content": ai_response})
			self._conversations[self._active_conversation] = messages
			return ai_response
		except Exception as e:
			# The user has already heard the specific error, so we just return the string
			# for display in the dialog's history. No new ui.message() is needed here.
			return str(e)


models = [
	PollinationsAI(),
	GPT4O(),
	GPT5Chat(),
	O4Mini(),
	O3(),
	O3Mini(),
	O3Pro(),
	GPT4Turbo(),
	GPT4(),
	Grok2Vision(),
	Claude4Sonnet(),
	Claude4Opus(),
	Claude3_7Sonnet(),
	Claude3_5SonnetV2(),
	Claude3_5Sonnet(),
	Claude3_5Haiku(),
	Claude3Haiku(),
	Claude3Sonnet(),
	Claude3Opus(),
	Gemini2_5FlashPreview(),
	Gemini2_5ProPreview(),
	Gemini2_0FlashLitePreview(),
	Gemini2_0Flash(),
	Gemini(),
	GeminiFlash1_5_8B(),
	Gemini1_5Pro(),
	PixtralLarge(),
	VivoBlueLMVision(),
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

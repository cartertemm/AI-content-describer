# Vision API interfaces for the AI Content Describer NVDA add-on
# Copyright (C) 2023 - 2026, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import base64
import json
import functools
import os
import time
import urllib.error
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
	log.warning(
		"Couldn't initialise translations. Is this addon running from NVDA's scratchpad directory?"
	)

import config_handler as ch
import cache
from computer_use import SYSTEM_PROMPT, format_focus_context

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


class StepResult:
	"""Represents a single call to a model following a computer-use request."""

	def __init__(self, text, actions, is_complete, pending):
		self.text = text
		self.actions = actions
		self.is_complete = is_complete
		self.pending = pending


def encode_image(image_path):
	with open(image_path, "rb") as image_file:
		return base64.b64encode(image_file.read()).decode("utf-8")


def detect_image_media_type(base64_data):
	"""Detect the media type of an image from its base64-encoded data.

	Examines magic bytes to determine the actual image format rather than
	relying on file extensions, which may not match the image content
	(e.g. clipboard images).
	"""
	header = base64.b64decode(base64_data[:32])
	if header[:3] == b"\xff\xd8\xff":
		return "image/jpeg"
	if header[:8] == b"\x89PNG\r\n\x1a\n":
		return "image/png"
	if header[:4] == b"GIF8":
		return "image/gif"
	if header[:4] == b"RIFF" and header[8:12] == b"WEBP":
		return "image/webp"
	return "image/png"


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

	# translators: error
	error = _("error")
	try:
		response = urllib.request.urlopen(*args, **kwargs).read()
	except IOError as i:
		tones.beep(150, 200)
		# translators: message spoken when we can't connect (error with connection)
		error_connection = _("error making connection")
		if str(i).find("Errno 11001") > -1:
			ui.message(error_connection)
		elif str(i).find("Errno 10060") > -1:
			ui.message(error_connection)
		elif str(i).find("Errno 10061") > -1:
			# translators: message spoken when the connection is refused by our target
			ui.message(_("error, connection refused by target"))
		else:
			reason = str(i)
			if hasattr(i, "fp"):
				error_text = i.fp.read()
				error_text = json.loads(error_text)
				if "error" in error_text:
					err = error_text["error"]
					if isinstance(err, dict) and "message" in err:
						reason += ". " + err["message"]
					elif isinstance(err, str):
						reason += ". " + err
			ui.message(error + ": " + reason)
			raise
		return
	except Exception as i:
		tones.beep(150, 200)
		ui.message(error + ": " + str(i))
		return
	return response


def post(**kwargs):
	"""Post to a URL and report status information back to NVDA.
	Keyword arguments are the same as those accepted by urllib.request.Request, except for timeout, which is handled separately.
	"""
	import ui
	import tones

	# translators: error
	error = _("error")
	# Callers that report errors themselves (the computer-use loop, which may have
	# already abandoned this request) pass quiet=True so we raise instead of speaking.
	quiet = kwargs.pop("quiet", False)
	kwargs["method"] = "POST"
	if "timeout" in kwargs:
		timeout = kwargs.get("timeout", 10)
		del kwargs["timeout"]
	else:
		timeout = 10
	try:
		request = urllib.request.Request(**kwargs)
		response = urllib.request.urlopen(request, timeout=timeout).read()
	except IOError as i:
		if quiet:
			detail = str(i)
			fp = getattr(i, "fp", None)
			if fp is not None:
				try:
					body = json.loads(fp.read().decode("utf-8"))
					err = body.get("error")
					if isinstance(err, dict):
						err = err.get("message")
					if err:
						detail += ". " + str(err)
				except Exception:
					pass
			raise IOError(detail) from i
		tones.beep(150, 200)
		# translators: message spoken when we can't connect (error with connection)
		error_connection = _("error making connection")
		if str(i).find("Errno 11001") > -1:
			ui.message(error_connection)
		elif str(i).find("Errno 10060") > -1:
			ui.message(error_connection)
		elif str(i).find("Errno 10061") > -1:
			# translators: message spoken when the connection is refused by our target
			ui.message(_("error, connection refused by target"))
		else:
			reason = str(i)
			if hasattr(i, "fp"):
				error_text = i.fp.read()
				log.debug(error_text)
				error_text = json.loads(error_text)
				if "error" in error_text:
					err = error_text["error"]
					if isinstance(err, dict) and "message" in err:
						reason += ". " + err["message"]
					elif isinstance(err, str):
						reason += ". " + err
			ui.message(error + ": " + reason)
			raise
		return
	except Exception as i:
		if quiet:
			raise
		tones.beep(150, 200)
		ui.message(error + ": " + str(i))
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
	supports_computer_use = False
	effort_levels = []

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
	def effort(self):
		return ch.config[self.name].get("effort")

	@effort.setter
	def effort(self, value):
		ch.config[self.name]["effort"] = value

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
		if (self.needs_api_key and self.api_key) or (
			self.needs_base_url and self.base_url
		):
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
						{
							"type": "image_url",
							"image_url": {
								"url": f"data:image/jpeg;base64,{msg['image']}"
							},
						},
					],
				}
			else:
				# a text-only message
				formatted_msg = {"role": msg["role"], "content": msg["content"]}
			formatted_messages.append(formatted_msg)
		payload = {
			"model": getattr(self, "internal_model_name", self.name),
			"messages": formatted_messages,
		}
		effective_max = kw.get("max_tokens", self.max_tokens)
		if effective_max is not None:
			payload[self._get_completion_token_param_name()] = effective_max
		return payload

	def _get_completion_token_param_name(self):
		"""Returns the output token field name for the chat completions request. Only the default build_conversation_payload calls this, so providers that override that method are unaffected."""
		netloc = urllib.parse.urlparse(self._get_conversation_url()).netloc.lower()
		if netloc == "api.openai.com":
			return "max_completion_tokens"
		return "max_tokens"

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

	def start_conversation(
		self, image_path=None, initial_prompt=None, initial_response=None
	):
		"""Start a new conversation, optionally with an image"""
		messages = []
		if image_path and initial_prompt and initial_response:
			# We have an image/initial prompt and response i.e. a description
			image_hash = get_image_hash(image_path)
			base64_image = encode_image(image_path)
			messages = [
				{"role": "user", "content": initial_prompt, "image": base64_image},
				{"role": "assistant", "content": initial_response},
			]
			self._conversations[image_hash] = messages
			self._active_conversation = image_hash
		elif initial_prompt and initial_response:
			# Text only
			conversation_id = "text_chat_" + str(len(self._conversations))
			messages = [
				{"role": "user", "content": initial_prompt},
				{"role": "assistant", "content": initial_response},
			]
			self._conversations[conversation_id] = messages
			self._active_conversation = conversation_id
		else:
			# Empty conversation: edge case
			conversation_id = "empty_chat_" + str(len(self._conversations))
			self._conversations[conversation_id] = []
			self._active_conversation = conversation_id

	def add_to_conversation(
		self, user_message, image_path=None, include_original_image=True
	):
		"""Add user message and get AI response. Returns the AI's response."""
		if (
			not self._active_conversation
			or self._active_conversation not in self._conversations
		):
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
		response = post(
			url=url,
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self.timeout,
		)
		response_json = json.loads(response.decode("utf-8"))
		ai_response = self._extract_conversation_response(response_json)
		messages.append({"role": "assistant", "content": ai_response})
		self._conversations[self._active_conversation] = messages
		return ai_response

	def has_conversation(self):
		"""Check if there's an active conversation for follow-ups"""
		return (
			self._active_conversation is not None
			and self._active_conversation in self._conversations
			and len(self._conversations[self._active_conversation]) > 0
		)

	def get_conversation_summary(self):
		"""Get a simple summary of the current conversation (for debugging)"""
		if not self.has_conversation():
			return "No active conversation"
		messages = self._conversations[self._active_conversation]
		return (
			f"Conversation with {len(messages)} messages (last: {messages[-1]['role']})"
		)

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

	def create_computer_session(self, task):
		raise NotImplementedError

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
				log.debug(
					f"Cache hit. Using cached description for {image_path} from {self.name}"
				)
				# Start a conversation in case the user wishes to follow-up
				self.start_conversation(image_path, self.prompt, description)
				return description
		# delegate to the wrapped description service
		log.debug(f"Cache miss. Fetching description for {image_path} from {self.name}")
		description = func(self, image_path, **kw)
		# (optionally) update the cache
		if is_cache_enabled and description:
			cache.read_cache(self.name)
			cache.cache[self.name][base64_image] = description
			cache.write_cache(self.name)
		return description

	return wrapper


def _normalize_openai_action(raw):
	"""Normalize an OpenAI Responses API computer_call action to our internal format.

	OpenAI uses:
	- "click" type with a "button" field and "coordinate": [x, y]
	- "key" type with a "keys": [...] array
	- "scroll" type with "scroll_direction" / "scroll_distance"
	- "coordinate": [x, y] instead of separate x/y fields
	- "drag" type with a "path": [[x, y], ...] or [{"x": x, "y": y}, ...] array,
	  using only the first and last point since we don't replay intermediate waypoints

	We also handle the alternative format where the action type is the dict key
	rather than a "type" field value.
	"""
	action = dict(raw)
	# Detect format where action type is the key, not a "type" field value
	# e.g. {"left_click": {"x": 100, "y": 200}}
	if not action.get("type"):
		for key, val in list(action.items()):
			if isinstance(val, dict):
				action["type"] = key
				action.update(val)
				del action[key]
				break
	t = action.get("type", "")
	if t == "click":
		button = action.pop("button", "left")
		action["type"] = f"{button}_click"
	coord = action.pop("coordinate", None)
	if coord and len(coord) >= 2:
		action["x"] = coord[0]
		action["y"] = coord[1]
	start = action.pop("start_coordinate", None)
	if start and len(start) >= 2:
		action["startX"] = start[0]
		action["startY"] = start[1]
	end = action.pop("end_coordinate", None)
	if end and len(end) >= 2:
		action["endX"] = end[0]
		action["endY"] = end[1]
	path = action.pop("path", None)
	if path and len(path) >= 2:

		def _point(p):
			if isinstance(p, dict):
				return p["x"], p["y"]
			return p[0], p[1]

		action["type"] = "left_click_drag"
		action["startX"], action["startY"] = _point(path[0])
		action["endX"], action["endY"] = _point(path[-1])
	if action.get("type") == "keypress":
		action["type"] = "key"
	keys = action.pop("keys", None)
	if keys:
		action["key"] = "+".join(k.lower() for k in keys)
	if "scroll_direction" in action:
		action["direction"] = action.pop("scroll_direction")
	if "scroll_distance" in action:
		action["amount"] = action.pop("scroll_distance")
	return action


class OpenAIComputerSession:
	"""Per-task conversation state for OpenAI computer use (Responses API)."""

	def __init__(self, service, task):
		self._service = service
		self._task = task
		self._previous_response_id = None

	def step(
		self,
		screenshot_b64,
		capture_w,
		capture_h,
		tool_results,
		injected_text,
		focus=None,
	):
		focus_text = format_focus_context(focus) if focus else ""
		headers = {
			"Authorization": f"Bearer {self._service.api_key}",
			"Content-Type": "application/json",
		}
		if tool_results:
			input_items = [
				{
					"type": "computer_call_output",
					"call_id": tr["call_id"],
					"output": {
						"type": "computer_screenshot",
						"image_url": f"data:image/png;base64,{screenshot_b64}",
					},
					"acknowledged_safety_checks": tr.get("safety_checks", []),
				}
				for tr in tool_results
			]
			if focus_text:
				input_items.append(
					{
						"type": "message",
						"role": "user",
						"content": [{"type": "input_text", "text": focus_text}],
					}
				)
		elif injected_text:
			# The model yielded and the user sent a follow-up
			# The computer tool rejects an input_image once a previous response exists, so we need to rely on the
			# model to request one when it needs to see the screen
			input_items = []
		else:
			input_items = [
				{
					"type": "message",
					"role": "user",
					"content": [
						{"type": "input_text", "text": self._task},
					]
					+ (
						[{"type": "input_text", "text": focus_text}]
						if focus_text
						else []
					)
					+ [
						{
							"type": "input_image",
							"image_url": f"data:image/png;base64,{screenshot_b64}",
							"detail": "original",
						},
					],
				}
			]
		if injected_text:
			input_items.append(
				{
					"type": "message",
					"role": "user",
					"content": [{"type": "input_text", "text": injected_text}],
				}
			)
		payload = {
			"model": self._service.internal_model_name,
			"tools": [{"type": "computer"}],
			"input": input_items,
			"instructions": SYSTEM_PROMPT,
		}
		if self._previous_response_id is not None:
			payload["previous_response_id"] = self._previous_response_id
		raw = post(
			url=OPENAI_RESPONSES_URL,
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self._service.timeout,
			quiet=True,
		)
		data = json.loads(raw.decode("utf-8"))
		log.debug(f"OpenAI computer use response: {json.dumps(data)}")
		text = ""
		actions = []
		for item in data.get("output", []):
			if item.get("type") == "message":
				for block in item.get("content", []):
					if block.get("type") == "output_text":
						text += block.get("text", "")
			elif item.get("type") == "computer_call":
				call_id = item.get("call_id", "")
				safety_checks = item.get("pending_safety_checks", [])
				for raw_action in item.get("actions", []):
					log.debug(f"Computer call action raw: {raw_action}")
					action = _normalize_openai_action(raw_action)
					action["call_id"] = call_id
					action["safety_checks"] = safety_checks
					actions.append(action)
		is_complete = data.get("stop_reason") == "completed" and not actions
		return StepResult(text, actions, is_complete, pending=data.get("id"))

	def save(self, step_result):
		if step_result.pending is not None:
			self._previous_response_id = step_result.pending


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
		headers = {"Content-Type": "application/json", "User-Agent": "curl/8.4.0"}
		if self.needs_api_key:
			headers["Authorization"] = f"Bearer {self.api_key}"
		return headers

	def _get_conversation_url(self):
		return getattr(self, "openai_url", "https://api.openai.com/v1/chat/completions")

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		prompt = kw.get("prompt") or self.prompt
		messages = [{"role": "user", "content": prompt, "image": base64_image}]
		payload = self.build_conversation_payload(
			messages, max_tokens=kw.get("max_tokens", self.max_tokens)
		)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(
			url=url,
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self.timeout,
		)
		response_json = json.loads(response.decode("utf-8"))
		content = self._extract_conversation_response(response_json)
		if not content:
			import ui

			ui.message("content returned none")
			return
		self.start_conversation(image_path, prompt, content)
		return content

	def create_computer_session(self, task):
		return OpenAIComputerSession(self, task)


class GPT4Turbo(BaseGPT):
	name = "GPT-4 turbo"
	# translators: the description for the GPT4 turbo model in the model configuration dialog
	description = _(
		"The next generation of the original GPT4 vision preview, with enhanced quality and understanding. This model will soon be deprecated so we recommend switching to GPT-4o."
	)
	about_url = (
		"https://help.openai.com/en/articles/8555510-gpt-4-turbo-in-the-openai-api"
	)
	internal_model_name = "gpt-4-turbo"


class GPT4O(BaseGPT):
	name = "GPT-4 omni"
	# translators: the description for the GPT4 omni model in the model configuration dialog
	description = _(
		"OpenAI's first fully multimodal model, released in May 2024. This model has the same high intelligence as GPT4 and GPT4 turbo, but is much more efficient, able to generate text at twice the speed and at half the cost."
	)
	about_url = "https://openai.com/index/hello-gpt-4o/"
	internal_model_name = "gpt-4o"


class GPT41(BaseGPT):
	name = "GPT-4.1"
	# translators: the description for the GPT-4.1 model in the configuration dialog
	description = _(
		"GPT-4.1 excels at instruction following and tool calling, with broad knowledge across domains. It features a 1M token context window, and low latency without a reasoning step."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-4.1"
	internal_model_name = "gpt-4.1"


class GPT41Mini(BaseGPT):
	name = "GPT-4.1 mini"
	# translators: the description for the GPT-4.1 mini model in the configuration dialog
	description = _(
		"A smaller, faster variant of GPT-4.1 with strong instruction following and a 1M token context window at reduced cost."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-4.1-mini"
	internal_model_name = "gpt-4.1-mini"


class GPT41Nano(BaseGPT):
	name = "GPT-4.1 nano"
	# translators: the description for the GPT-4.1 nano model in the configuration dialog
	description = _(
		"The smallest and most affordable GPT-4.1 variant, optimized for fast responses with a 1M token context window."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-4.1-nano"
	internal_model_name = "gpt-4.1-nano"


class GPT5(BaseGPT):
	name = "GPT-5"
	# translators: the description for the GPT-5 model in the configuration dialog
	description = _(
		"OpenAI's frontier model with advanced reasoning, vision, and a 400k token context window."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-5"
	internal_model_name = "gpt-5"


class GPT5Mini(BaseGPT):
	name = "GPT-5 mini"
	# translators: the description for the GPT-5 mini model in the configuration dialog
	description = _(
		"A fast, cost-efficient variant of GPT-5 with vision support and a 400k token context window."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-5-mini"
	internal_model_name = "gpt-5-mini"


class GPT5Nano(BaseGPT):
	name = "GPT-5 nano"
	# translators: the description for the GPT-5 nano model in the configuration dialog
	description = _(
		"The smallest GPT-5 variant, offering vision capabilities at the lowest cost."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-5-nano"
	internal_model_name = "gpt-5-nano"


class GPT5Chat(BaseGPT):
	name = "GPT-5 chat"
	# translators: the description for the GPT‑5 chat model in the configuration dialog
	description = _("GPT-5 model used in ChatGPT")
	about_url = "https://platform.openai.com/docs/models/gpt-5-chat-latest"
	internal_model_name = "gpt-5-chat-latest"


class GPT54(BaseGPT):
	name = "GPT-5.4"
	# translators: the description for the GPT-5.4 model in the configuration dialog
	description = _(
		"OpenAI's latest flagship model with advanced reasoning, vision, and a 400k token context window."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-5.4"
	internal_model_name = "gpt-5.4"
	supports_computer_use = True


class GPT54Mini(BaseGPT):
	name = "GPT-5.4 mini"
	# translators: the description for the GPT-5.4 mini model in the configuration dialog
	description = _(
		"A fast, affordable variant of GPT-5.4 with vision support and a 400k token context window."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-5.4-mini"
	internal_model_name = "gpt-5.4-mini"
	supports_computer_use = True


class GPT54Nano(BaseGPT):
	name = "GPT-5.4 nano"
	# translators: the description for the GPT-5.4 nano model in the configuration dialog
	description = _(
		"The smallest and cheapest GPT-5.4 variant with vision capabilities and a 400k token context window."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-5.4-nano"
	internal_model_name = "gpt-5.4-nano"
	supports_computer_use = True


class GPT55(BaseGPT):
	name = "GPT-5.5"
	# translators: the description for the GPT-5.5 model in the configuration dialog
	description = _(
		"OpenAI's frontier model for complex professional work, with a new class of intelligence for coding, vision, and agentic tasks. Supports image input and a 1M token context window."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-5.5"
	internal_model_name = "gpt-5.5"
	supports_computer_use = True


class GPT55Pro(BaseGPT):
	name = "GPT-5.5 pro"
	# translators: the description for the GPT-5.5 pro model in the configuration dialog
	description = _(
		"A higher-compute variant of GPT-5.5 that thinks harder for smarter and more precise responses on complex, high-stakes workloads. Supports image input and a 1M token context window."
	)
	about_url = "https://platform.openai.com/docs/models/gpt-5.5-pro"
	internal_model_name = "gpt-5.5-pro"
	supports_computer_use = True


class O3(BaseGPT):
	name = "OpenAI O3"
	# translators: the description for the OpenAI O3 model in the model configuration dialog
	description = _(
		"Released in April 2025, o3 is a well-rounded and powerful model across domains. It sets a new standard for math, science, coding, and visual reasoning tasks. It also excels at technical writing and instruction-following. Use it to think through multi-step problems that involve analysis across text, code, and images."
	)
	about_url = "https://openai.com/index/introducing-o3-and-o4-mini/"
	internal_model_name = "o3"


class O3Pro(BaseGPT):
	name = "OpenAI O3 pro"
	# translators: the description for the OpenAI O3 pro model in the model configuration dialog
	description = _(
		"Released in June 2025, O3 pro is an upgraded version of O3. It is designed to think longer and provide the most reliable responses. Because o3-pro has access to tools, responses typically take longer than o1-pro to complete. We recommend using it for challenging questions where reliability matters more than speed, and waiting a few minutes is worth the tradeoff. Do not forget to tweak the timeout setting."
	)
	about_url = "https://help.openai.com/en/articles/9624314-model-release-notes"
	internal_model_name = "o3-pro"


class O3Mini(BaseGPT):
	name = "OpenAI O3 mini"
	# translators: the description for the OpenAI O3 mini model in the model configuration dialog
	description = _(
		"Released in January 2025, this powerful and fast model advances the boundaries of what small models can achieve, delivering exceptional STEM capabilities with particular strength in science, math, and coding all while maintaining the low cost and reduced latency of OpenAI o1-mini."
	)
	about_url = "https://openai.com/index/openai-o3-mini/"
	internal_model_name = "o3-mini"


class O4Mini(BaseGPT):
	name = "OpenAI O4 mini"
	# translators: the description for the OpenAI O4 mini model in the model configuration dialog
	description = _(
		"Released in April 2025, o4-mini is a smaller model optimized for fast, cost-efficient reasoning. It achieves remarkable performance for its size and cost, particularly in math, coding, and visual tasks. It has been shown to outperform O3 mini and supports significantly higher usage limits than o3, making it a strong high-volume, high-throughput option for questions that benefit from reasoning. Do not forget to tweak the timeout setting."
	)
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
				parts.insert(
					0,
					{"inline_data": {"mime_type": "image/jpeg", "data": msg["image"]}},
				)
			role = msg["role"]
			if role == "assistant":
				role = "model"  # Google refers to the assistant role as "model"
			contents.append({"role": role, "parts": parts})
		gen_config = {}
		effective_max = kw.get("max_tokens", self.max_tokens)
		if effective_max is not None:
			gen_config["maxOutputTokens"] = effective_max
		return {"contents": contents, "generationConfig": gen_config}

	def _get_conversation_url(self):
		return f"https://generativelanguage.googleapis.com/v1beta/models/{self.internal_model_name}:generateContent?key={self.api_key}"

	def _get_conversation_headers(self):
		return {"Content-Type": "application/json"}

	def _extract_conversation_response(self, response_json):
		if "error" in response_json:
			import ui

			# translators: message spoken when Google gemini encounters an error with the format or content of the input.
			ui.message(
				_("Gemini encountered an error: {code}, {msg}").format(
					code=response_json["error"]["code"],
					msg=response_json["error"]["message"],
				)
			)
			return ""
		try:
			return response_json["candidates"][0]["content"]["parts"][0]["text"]
		except (KeyError, IndexError):
			import ui

			# translators: message spoken when a Gemini thinking model uses all its tokens for reasoning, leaving nothing for the visible response. The user should increase max tokens in settings.
			ui.message(
				_(
					"The model used all available tokens for reasoning and returned no visible response. Try increasing the max tokens setting."
				)
			)
			return ""

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		prompt = kw.get("prompt") or self.prompt
		messages = [{"role": "user", "content": prompt, "image": base64_image}]
		payload = self.build_conversation_payload(
			messages, max_tokens=kw.get("max_tokens", self.max_tokens)
		)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(
			url=url,
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self.timeout,
		)
		response_json = json.loads(response.decode("utf-8"))
		content = self._extract_conversation_response(response_json)
		if not content:
			return
		self.start_conversation(image_path, prompt, content)
		return content


class Gemini2_5Flash(GoogleGemini):
	name = "Google Gemini 2.5 Flash"
	internal_model_name = "gemini-2.5-flash"
	# translators: the description for Google's Gemini 2.5 Flash model, as shown in the configuration dialog.
	description = _(
		"Gemini 2.5 Flash delivers fast performance for complex tasks. Ideal for tasks like summarization, chat applications, data extraction, and captioning."
	)
	about_url = "https://deepmind.google/models/gemini/flash/"


class Gemini2_5FlashLite(GoogleGemini):
	name = "Google Gemini 2.5 Flash-Lite"
	internal_model_name = "gemini-2.5-flash-lite"
	# translators: the description for Google's Gemini 2.5 Flash-Lite model, as shown in the configuration dialog.
	description = _(
		"Gemini 2.5 Flash-Lite is optimized for cost efficiency and low latency while maintaining strong performance."
	)
	about_url = "https://deepmind.google/models/gemini/flash-lite/"


class Gemini2_5Pro(GoogleGemini):
	name = "Google Gemini 2.5 Pro"
	internal_model_name = "gemini-2.5-pro"
	# translators: the description for Google's Gemini 2.5 Pro model, as shown in the configuration dialog.
	description = _(
		"Gemini 2.5 Pro models are capable of reasoning through their thoughts before responding, resulting in enhanced performance and improved accuracy. Best for coding and complex tasks."
	)
	about_url = "https://deepmind.google/models/gemini/pro/"


class Gemini3FlashPreview(GoogleGemini):
	name = "Google Gemini 3 Flash Preview"
	internal_model_name = "gemini-3-flash-preview"
	# translators: the description for Google's Gemini 3 Flash Preview model, as shown in the configuration dialog.
	description = _(
		"Gemini 3 Flash is Google's latest multimodal model with strong vision and agentic capabilities. Supports text, image, video, audio, and PDF input with a 1M token context window."
	)
	about_url = "https://deepmind.google/models/gemini/flash/"


class Gemini3_1FlashLitePreview(GoogleGemini):
	name = "Google Gemini 3.1 Flash-Lite Preview"
	internal_model_name = "gemini-3.1-flash-lite-preview"
	# translators: the description for Google's Gemini 3.1 Flash-Lite Preview model, as shown in the configuration dialog.
	description = _(
		"Gemini 3.1 Flash-Lite is the most cost-efficient model in the Gemini 3 series, designed for high volume tasks."
	)
	about_url = "https://deepmind.google/models/gemini/flash-lite/"


class Gemini3_1ProPreview(GoogleGemini):
	name = "Google Gemini 3.1 Pro Preview"
	internal_model_name = "gemini-3.1-pro-preview"
	# translators: the description for Google's Gemini 3.1 Pro Preview model, as shown in the configuration dialog.
	description = _(
		"Gemini 3.1 Pro is Google's latest reasoning-first model for complex agentic workflows, with enhanced performance and accuracy."
	)
	about_url = "https://deepmind.google/models/gemini/pro/"


class Gemini3_5Flash(GoogleGemini):
	name = "Google Gemini 3.5 Flash"
	internal_model_name = "gemini-3.5-flash"
	# translators: the description for Google's Gemini 3.5 Flash model, as shown in the configuration dialog.
	description = _(
		"Gemini 3.5 Flash is Google's latest and most capable Flash model, with faster response times and reduced latency. Ideal for tasks requiring both speed and quality."
	)
	about_url = "https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash"


class AnthropicComputerSession:
	"""Per-task conversation state for Anthropic computer use."""

	# Any more than this number of screenshots will be deleted to save API quota. Models are hungry.
	KEEP_RECENT_SCREENSHOTS = 3

	def __init__(self, service, task):
		self._service = service
		self._task = task
		self._history = []

	def _build_user_turn(self, screenshot_b64, tool_results, injected_text, focus_text):
		"""Return the user-turn dict for this step, or None if there's nothing to add."""
		if not self._history:
			content = [
				{"type": "text", "text": self._task},
				{
					"type": "image",
					"source": {
						"type": "base64",
						"media_type": "image/png",
						"data": screenshot_b64,
					},
				},
			]
			if focus_text:
				content.insert(1, {"type": "text", "text": focus_text})
			return {"role": "user", "content": content}
		content_blocks = [
			{
				"type": "tool_result",
				"tool_use_id": tr["call_id"],
				"content": [
					{
						"type": "image",
						"source": {
							"type": "base64",
							"media_type": "image/png",
							"data": screenshot_b64,
						},
					},
					{"type": "text", "text": tr["compact_result"]},
				],
			}
			for tr in (tool_results or [])
		]
		if focus_text and content_blocks:
			content_blocks.append({"type": "text", "text": focus_text})
		if injected_text:
			content_blocks.append({"type": "text", "text": injected_text})
		if not content_blocks:
			return None
		return {"role": "user", "content": content_blocks}

	def step(
		self,
		screenshot_b64,
		capture_w,
		capture_h,
		tool_results,
		injected_text,
		focus=None,
	):
		focus_text = format_focus_context(focus) if focus else ""
		new_user_turn = self._build_user_turn(
			screenshot_b64, tool_results, injected_text, focus_text
		)
		messages = self._history + ([new_user_turn] if new_user_turn else [])
		headers = {
			"x-api-key": self._service.api_key,
			"anthropic-version": "2023-06-01",
			"anthropic-beta": self._service._computer_use_beta,
			"Content-Type": "application/json",
		}
		tool_def = {
			"type": self._service._computer_use_tool_type,
			"name": "computer",
			"display_width_px": capture_w,
			"display_height_px": capture_h,
		}
		payload = {
			"model": self._service.internal_model_name,
			"max_tokens": 16384 if self._service._thinks_by_default else 4096,
			"system": SYSTEM_PROMPT,
			"tools": [tool_def],
			"messages": messages,
		}
		raw = post(
			url="https://api.anthropic.com/v1/messages",
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self._service.timeout,
			quiet=True,
		)
		data = json.loads(raw.decode("utf-8"))
		text = ""
		actions = []
		for block in data.get("content", []):
			if block.get("type") == "text":
				text += block.get("text", "")
			elif block.get("type") == "tool_use" and block.get("name") == "computer":
				inp = block.get("input", {})
				action = {
					"type": inp.get("action", ""),
					"call_id": block.get("id", ""),
					"safety_checks": [],
				}
				coord = inp.get("coordinate")
				if coord:
					action["x"], action["y"] = coord[0], coord[1]
				start = inp.get("start_coordinate")
				if start:
					action["startX"], action["startY"] = start[0], start[1]
				end = inp.get("end_coordinate")
				if end:
					action["endX"], action["endY"] = end[0], end[1]
				for k in ("text", "key", "direction", "amount"):
					if k in inp:
						action[k] = inp[k]
				actions.append(action)
		assistant_turn = {"role": "assistant", "content": data.get("content", [])}
		is_complete = data.get("stop_reason") == "end_turn" and not actions
		pending = [t for t in (new_user_turn, assistant_turn) if t]
		return StepResult(text, actions, is_complete, pending=pending)

	def save(self, step_result):
		self._history.extend(step_result.pending)
		self._trim_history_screenshots(self._history)

	def _trim_history_screenshots(self, history):
		"""Remove all but the most recent screenshot image blocks from history, including those nested in tool_result blocks."""
		refs = []
		for i, msg in enumerate(history):
			for j, block in enumerate(msg.get("content") or []):
				if not isinstance(block, dict):
					continue
				if block.get("type") == "image":
					refs.append((i, j, None))
				elif block.get("type") == "tool_result":
					for k, inner in enumerate(block.get("content") or []):
						if isinstance(inner, dict) and inner.get("type") == "image":
							refs.append((i, j, k))
		for i, j, k in reversed(refs[: -self.KEEP_RECENT_SCREENSHOTS]):
			if k is None:
				history[i]["content"].pop(j)
			else:
				history[i]["content"][j]["content"].pop(k)


class Anthropic(BaseDescriptionService):
	supported_formats = [".jpeg", ".jpg", ".png", ".gif", ".webp"]
	# Models that run adaptive thinking when the request omits the thinking parameter.
	# Thinking tokens count against max_tokens, so these need more headroom.
	_thinks_by_default = False

	def build_conversation_payload(self, messages, **kw):
		"""Override for Anthropic's message format with content arrays"""
		formatted_messages = []
		for msg in messages:
			content = [{"type": "text", "text": msg["content"]}]
			if msg.get("image"):
				content.insert(
					0,
					{
						"type": "image",
						"source": {
							"type": "base64",
							"media_type": detect_image_media_type(msg["image"]),
							"data": msg["image"],
						},
					},
				)
			formatted_messages.append({"role": msg["role"], "content": content})
		effective_max = kw.get("max_tokens", self.max_tokens)
		payload = {
			"model": self.internal_model_name,
			"messages": formatted_messages,
			"max_tokens": effective_max if effective_max is not None else 32768,
		}
		if self.effort_levels and self.effort:
			payload["output_config"] = {"effort": self.effort}
		return payload

	def _get_conversation_url(self):
		return "https://api.anthropic.com/v1/messages"

	def _get_conversation_headers(self):
		return {
			"User-Agent": "curl/8.4.0",
			"Content-Type": "application/json",
			"x-api-key": self.api_key,
			"anthropic-version": "2023-06-01",
		}

	def _extract_conversation_response(self, response_json):
		if response_json.get("type") == "error":
			import ui

			# translators: message spoken when Claude encounters an error with the format or content of the input.
			ui.message(
				_("Claude encountered an error. {err}").format(
					err=response_json["error"]["message"]
				)
			)
			return ""
		for block in response_json.get("content", []):
			if block.get("type") == "text":
				return block["text"]
		return ""

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		prompt = kw.get("prompt") or self.prompt
		messages = [{"role": "user", "content": prompt, "image": base64_image}]
		payload = self.build_conversation_payload(
			messages, max_tokens=kw.get("max_tokens", self.max_tokens)
		)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(
			url=url,
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self.timeout,
		)
		response_json = json.loads(response.decode("utf-8"))
		content = self._extract_conversation_response(response_json)
		if not content:
			return
		self.start_conversation(image_path, prompt, content)
		return content

	def create_computer_session(self, task):
		return AnthropicComputerSession(self, task)


class Claude4_5Sonnet(Anthropic):
	name = "Claude 4.5 Sonnet"
	# translators: the description for the Claude 4.5 Sonnet model in the model configuration dialog
	description = _(
		"Anthropic's upgraded Sonnet with extended thinking capabilities and a strong balance of speed and intelligence."
	)
	about_url = "https://www.anthropic.com/claude/sonnet"
	internal_model_name = "claude-sonnet-4-5-20250929"
	supports_computer_use = True
	_computer_use_beta = "computer-use-2025-01-24"
	_computer_use_tool_type = "computer_20250124"
	_capture_max_long_edge = 1568
	_capture_max_pixels = 1_150_000


class Claude4_5Opus(Anthropic):
	name = "Claude 4.5 Opus"
	# translators: the description for the Claude 4.5 Opus model in the model configuration dialog
	description = _(
		"Anthropic's advanced Opus model with extended thinking and superior performance on complex tasks."
	)
	about_url = "https://www.anthropic.com/claude/opus"
	internal_model_name = "claude-opus-4-5-20251101"
	supports_computer_use = True
	effort_levels = ['low', 'medium', 'high']
	_computer_use_beta = "computer-use-2025-11-24"
	_computer_use_tool_type = "computer_20251124"
	_capture_max_long_edge = 1568
	_capture_max_pixels = 1_150_000


class Claude4_6Sonnet(Anthropic):
	name = "Claude 4.6 Sonnet"
	# translators: the description for the Claude 4.6 Sonnet model in the model configuration dialog
	description = _(
		"Anthropic's latest Sonnet model with the best combination of speed and intelligence. Features a 1M token context window and adaptive thinking."
	)
	about_url = "https://www.anthropic.com/claude/sonnet"
	internal_model_name = "claude-sonnet-4-6"
	supports_computer_use = True
	effort_levels = ['low', 'medium', 'high', 'max']
	_computer_use_beta = "computer-use-2025-11-24"
	_computer_use_tool_type = "computer_20251124"
	_capture_max_long_edge = 1568
	_capture_max_pixels = 1_150_000


class Claude4_6Opus(Anthropic):
	name = "Claude 4.6 Opus"
	# translators: the description for the Claude 4.6 Opus model in the model configuration dialog
	description = _(
		"Anthropic's most intelligent model for building agents and coding. Features a 1M token context window, extended thinking, and exceptional reasoning."
	)
	about_url = "https://www.anthropic.com/claude/opus"
	internal_model_name = "claude-opus-4-6"
	supports_computer_use = True
	effort_levels = ['low', 'medium', 'high', 'max']
	_computer_use_beta = "computer-use-2025-11-24"
	_computer_use_tool_type = "computer_20251124"
	_capture_max_long_edge = 1568
	_capture_max_pixels = 1_150_000


class Claude4_7Opus(Anthropic):
	name = "Claude 4.7 Opus"
	# translators: the description for the Claude 4.7 Opus model in the model configuration dialog
	description = _(
		"Anthropic's most capable generally available model. Features high-resolution vision support up to 3.75MP, adaptive thinking, and a 1M token context window."
	)
	about_url = "https://www.anthropic.com/claude/opus"
	internal_model_name = "claude-opus-4-7"
	supports_computer_use = True
	effort_levels = ['low', 'medium', 'high', 'xhigh', 'max']
	_computer_use_beta = "computer-use-2025-11-24"
	_computer_use_tool_type = "computer_20251124"
	_capture_max_long_edge = 2576
	_capture_max_pixels = None


class Claude4_8Opus(Anthropic):
	name = "Claude 4.8 Opus"
	# translators: the description for the Claude 4.8 Opus model in the model configuration dialog
	description = _(
		"Anthropic's refined Opus model with the same high-resolution vision, adaptive thinking, and 1M token context window as Claude 4.7 Opus."
	)
	about_url = "https://www.anthropic.com/claude/opus"
	internal_model_name = "claude-opus-4-8"
	supports_computer_use = True
	effort_levels = ['low', 'medium', 'high', 'xhigh', 'max']
	_computer_use_beta = "computer-use-2025-11-24"
	_computer_use_tool_type = "computer_20251124"
	_capture_max_long_edge = 2576
	_capture_max_pixels = None


class Claude5Sonnet(Anthropic):
	name = "Claude 5 Sonnet"
	# translators: the description for the Claude 5 Sonnet model in the model configuration dialog
	description = _(
		"Anthropic's fast and affordable Sonnet model with high-resolution vision, adaptive thinking, and a 1M token context window."
	)
	about_url = "https://www.anthropic.com/claude/sonnet"
	internal_model_name = "claude-sonnet-5"
	supports_computer_use = True
	effort_levels = ['low', 'medium', 'high', 'xhigh', 'max']
	_thinks_by_default = True
	_computer_use_beta = "computer-use-2025-11-24"
	_computer_use_tool_type = "computer_20251124"
	_capture_max_long_edge = 2576
	_capture_max_pixels = None


class Claude5Opus(Anthropic):
	name = "Claude 5 Opus"
	# translators: the description for the Claude 5 Opus model in the model configuration dialog
	description = _(
		"Anthropic's most capable Opus model. Thinks by default, with high-resolution vision and a 1M token context window."
	)
	about_url = "https://www.anthropic.com/claude/opus"
	internal_model_name = "claude-opus-5"
	supports_computer_use = True
	effort_levels = ['low', 'medium', 'high', 'xhigh', 'max']
	_thinks_by_default = True
	_computer_use_beta = "computer-use-2025-11-24"
	_computer_use_tool_type = "computer_20251124"
	_capture_max_long_edge = 2576
	_capture_max_pixels = None


class Claude5Fable(Anthropic):
	name = "Claude 5 Fable"
	# translators: the description for the Claude 5 Fable model in the model configuration dialog
	description = _(
		"Anthropic's frontier model above the Opus tier, for the most demanding reasoning and vision tasks. Thinking is always on. Higher cost than Opus."
	)
	about_url = "https://www.anthropic.com/claude/fable"
	internal_model_name = "claude-fable-5"
	supports_computer_use = True
	effort_levels = ['low', 'medium', 'high', 'xhigh', 'max']
	_thinks_by_default = True
	_computer_use_beta = "computer-use-2025-11-24"
	_computer_use_tool_type = "computer_20251124"
	_capture_max_long_edge = 2576
	_capture_max_pixels = None


class Claude5_1Fable(Anthropic):
	name = "Claude 5.1 Fable"
	# translators: the description for the Claude 5.1 Fable model in the model configuration dialog
	description = _(
		"Anthropic's most intelligent generally available model, with stronger vision and computer use than Claude 5 Fable. Thinking is always on. Higher cost than Opus."
	)
	about_url = "https://www.anthropic.com/claude/fable"
	internal_model_name = "claude-fable-5-1"
	supports_computer_use = True
	effort_levels = ['low', 'medium', 'high', 'xhigh', 'max']
	_thinks_by_default = True
	_computer_use_beta = "computer-use-2025-11-24"
	_computer_use_tool_type = "computer_20251124"
	_capture_max_long_edge = 2576
	_capture_max_pixels = None


class MistralAI(BaseDescriptionService):
	supported_formats = [".png", ".jpg", ".jpeg", ".webp", ".gif"]
	needs_api_key = True

	def _get_conversation_url(self):
		return "https://api.mistral.ai/v1/chat/completions"

	def _get_conversation_headers(self):
		return {
			"User-Agent": "curl/8.4.0",
			"Content-Type": "application/json",
			"Authorization": "Bearer " + self.api_key,
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
						{
							"type": "image_url",
							"image_url": f"data:image/jpeg;base64,{msg['image']}",
						},
					],
				}
			else:
				# Text-only message
				formatted_msg = {"role": msg["role"], "content": msg["content"]}
			formatted_messages.append(formatted_msg)
		payload = {
			"model": self.internal_model_name,
			"messages": formatted_messages,
		}
		effective_max = kw.get("max_tokens", self.max_tokens)
		if effective_max is not None:
			payload["max_tokens"] = effective_max
		return payload

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		prompt = kw.get("prompt") or self.prompt
		messages = [{"role": "user", "content": prompt, "image": base64_image}]
		payload = self.build_conversation_payload(
			messages, max_tokens=kw.get("max_tokens", self.max_tokens)
		)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(
			url=url,
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self.timeout,
		)
		response_json = json.loads(response.decode("utf-8"))
		content = self._extract_conversation_response(response_json)
		if not content:
			import ui

			ui.message("content returned none")
			return
		self.start_conversation(image_path, prompt, content)
		return content


class PixtralLarge(MistralAI):
	name = "Pixtral Large"
	# translators: the description for MistralAI's Pixtral Large model, as shown in the configuration dialog.
	description = _(
		"MistralAI's multimodal image LLM, achieving state-of-the-art results on MathVista, DocVQA, VQAv2 and other benchmarks."
	)
	internal_model_name = "pixtral-large-latest"
	about_url = "https://mistral.ai/news/pixtral-large/"


class Grok2Vision(BaseGPT):
	name = "Grok 2 vision"
	# translators: the description for the xAI Grok 2 model in the model configuration dialog
	description = _(
		"xAI's flagship multimodal model with advanced reasoning capabilities. Excels at enterprise tasks like data extraction, programming, and text summarization with superior domain knowledge in finance, healthcare, law, and science."
	)
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


class Grok4Base(BaseGPT):
	openai_url = "https://api.x.ai/v1/chat/completions"
	supported_formats = [
		".jpeg",
		".jpg",
		".png",
	]

	def _get_completion_token_param_name(self):
		# Grok 4 reasoning models require max_completion_tokens
		return "max_completion_tokens"


class Grok4(Grok4Base):
	name = "Grok 4"
	# translators: the description for the xAI Grok 4 model in the model configuration dialog
	description = _(
		"xAI's flagship multimodal reasoning model. Supports image input and excels at complex reasoning, math, science, and visual tasks."
	)
	about_url = "https://x.ai/news/grok-4"
	internal_model_name = "grok-4"


class Grok4FastReasoning(Grok4Base):
	name = "Grok 4 Fast (reasoning)"
	# translators: the description for the xAI Grok 4 Fast reasoning model in the model configuration dialog
	description = _(
		"xAI's cost-efficient multimodal reasoning model with a 2M token context window. Achieves performance comparable to Grok 4 with 40% fewer thinking tokens on average."
	)
	about_url = "https://x.ai/news/grok-4-fast"
	internal_model_name = "grok-4-fast-reasoning"


class Grok4FastNonReasoning(Grok4Base):
	name = "Grok 4 Fast (non-reasoning)"
	# translators: the description for the xAI Grok 4 Fast non-reasoning model in the model configuration dialog
	description = _(
		"xAI's cost-efficient multimodal model for instant responses without a reasoning step. Features a 2M token context window."
	)
	about_url = "https://x.ai/news/grok-4-fast"
	internal_model_name = "grok-4-fast-non-reasoning"


class Grok4_3(Grok4Base):
	name = "Grok 4.3"
	# translators: the description for the xAI Grok 4.3 model in the model configuration dialog
	description = _(
		"xAI's recommended flagship reasoning model with a 1M token context window. Features always-on chain-of-thought reasoning and support for image input."
	)
	about_url = "https://docs.x.ai/developers/models"
	internal_model_name = "grok-4.3"


class Kimi(BaseGPT):
	openai_url = "https://api.moonshot.ai/v1/chat/completions"
	supported_formats = [
		".gif",
		".jpeg",
		".jpg",
		".png",
		".webp",
	]


class KimiK3(Kimi):
	name = "Kimi K3"
	# translators: the description for Moonshot AI's Kimi K3 model in the model configuration dialog
	description = _(
		"Moonshot AI's flagship multimodal model, with a 1M token context window and strong reasoning across text, image, and video."
	)
	about_url = "https://platform.kimi.ai/docs/guide/use-kimi-vision-model"
	internal_model_name = "kimi-k3"


class KimiK2_6(Kimi):
	name = "Kimi K2.6"
	# translators: the description for Moonshot AI's Kimi K2.6 model in the model configuration dialog
	description = _(
		"A capable Kimi multimodal model that understands both image and video input alongside text."
	)
	about_url = "https://platform.kimi.ai/docs/guide/use-kimi-vision-model"
	internal_model_name = "kimi-k2.6"


class KimiK2_5(Kimi):
	name = "Kimi K2.5"
	# translators: the description for Moonshot AI's Kimi K2.5 model in the model configuration dialog
	description = _(
		"A Kimi multimodal model with image and text understanding, well suited to describing pictures and reading text within them."
	)
	about_url = "https://platform.kimi.ai/docs/guide/use-kimi-vision-model"
	internal_model_name = "kimi-k2.5"


class Ollama(BaseDescriptionService):
	name = "Ollama"
	needs_api_key = False
	needs_base_url = True
	# translators: the description for the Ollama model, as shown in the configuration dialog
	description = _(
		"The quickest way to get up and running with large language models."
	)
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
			ui.message(_("Could not contact the provided base URL. " + str(exc)))
			return
		content = json.loads(content)
		models = [model["model"] for model in content["models"]]
		return models

	def build_conversation_payload(self, messages, **kw):
		"""Override for Ollama's chat format with images array"""
		formatted_messages = []
		for msg in messages:
			formatted_msg = {"role": msg["role"], "content": msg["content"]}
			if msg.get("image"):
				formatted_msg["images"] = [msg["image"]]
			formatted_messages.append(formatted_msg)
		return {
			"model": self.chosen_model,
			"messages": formatted_messages,
			"stream": False,
		}

	def _get_conversation_url(self):
		return urllib.parse.urljoin(self.base_url, "api/chat")

	def _get_conversation_headers(self):
		return {"Content-Type": "application/json"}

	def _extract_conversation_response(self, response_json):
		if "message" not in response_json:
			import ui

			ui.message(
				_("The response appears to be malformed. " + repr(response_json))
			)
			return ""
		return response_json["message"]["content"]

	@cached_description
	def process(self, image_path, **kw):
		# Build single-image conversation
		base64_image = encode_image(image_path)
		prompt = kw.get("prompt") or self.prompt
		messages = [{"role": "user", "content": prompt, "image": base64_image}]
		# Use conversation methods for consistency
		payload = self.build_conversation_payload(messages)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(
			url=url,
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self.timeout,
		)
		response_json = json.loads(response.decode("utf-8"))
		content = self._extract_conversation_response(response_json)
		if not content:
			return
		self.start_conversation(image_path, prompt, content)
		return content


class LiteLLMProxy(BaseDescriptionService):
	name = "LiteLLM Proxy"
	needs_api_key = False
	needs_base_url = True
	# translators: the description for the LiteLLM Proxy model, as shown in the configuration dialog
	description = _("Access multiple AI models through a unified LiteLLM proxy server.")
	supported_formats = [
		".gif",
		".jpeg",
		".jpg",
		".png",
		".webp",
	]
	about_url = "https://docs.litellm.ai/docs/proxy/quick_start"

	def list_model_names(self, base_url, api_key=None):
		base_url = base_url or self.base_url
		api_key = api_key or self.api_key
		if not base_url:
			import ui

			# translators: the message spoken in the LiteLLM configuration dialog when no base URL is provided
			ui.message(_("Please provide a base URL first."))
			return

		url = urllib.parse.urljoin(base_url, "v1/models")
		headers = {"Content-Type": "application/json", "User-Agent": "curl/8.4.0"}
		if api_key:
			headers["Authorization"] = f"Bearer {api_key}"

		try:
			request = urllib.request.Request(url, headers=headers)
			content = urllib.request.urlopen(request).read()
		except Exception as exc:
			import ui

			# translators: the message spoken in the LiteLLM configuration dialog upon pressing "list models", when the proxy cannot be contacted.
			ui.message(_("Could not contact the LiteLLM proxy server. " + str(exc)))
			return

		try:
			content = json.loads(content)
			models = [model["id"] for model in content.get("data", [])]
			return models
		except (json.JSONDecodeError, KeyError) as exc:
			import ui

			# translators: the message spoken when the LiteLLM proxy returns an unexpected response format
			ui.message(_("Unexpected response format from LiteLLM proxy. " + str(exc)))
			return

	def build_conversation_payload(self, messages, **kw):
		"""Build OpenAI-compatible payload for LiteLLM proxy"""
		formatted_messages = []
		for msg in messages:
			formatted_msg = {"role": msg["role"], "content": []}

			# Add text content
			if msg.get("content"):
				formatted_msg["content"].append(
					{"type": "text", "text": msg["content"]}
				)

			# Add image content if present
			if msg.get("image"):
				formatted_msg["content"].append(
					{
						"type": "image_url",
						"image_url": {"url": f"data:image/jpeg;base64,{msg['image']}"},
					}
				)

			formatted_messages.append(formatted_msg)

		payload = {"messages": formatted_messages, "stream": False}
		effective_max = kw.get("max_tokens", self.max_tokens)
		if effective_max is not None:
			payload["max_tokens"] = effective_max
		# Add model if specified
		if self.chosen_model:
			payload["model"] = self.chosen_model
		return payload

	def _get_conversation_url(self):
		return urllib.parse.urljoin(self.base_url, "v1/chat/completions")

	def _get_conversation_headers(self):
		headers = {"Content-Type": "application/json", "User-Agent": "curl/8.4.0"}
		if self.api_key:
			headers["Authorization"] = f"Bearer {self.api_key}"
		return headers

	def _extract_conversation_response(self, response_json):
		if (
			"choices" not in response_json
			or not response_json["choices"]
			or "message" not in response_json["choices"][0]
		):
			import ui

			ui.message(
				_("The response appears to be malformed. " + repr(response_json))
			)
			return ""
		return response_json["choices"][0]["message"]["content"]

	@cached_description
	def process(self, image_path, **kw):
		"""Process an image through the LiteLLM proxy and return a description"""
		base64_image = encode_image(image_path)
		prompt = kw.get("prompt") or self.prompt
		messages = [{"role": "user", "content": prompt, "image": base64_image}]
		payload = self.build_conversation_payload(
			messages, max_tokens=kw.get("max_tokens", self.max_tokens)
		)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(
			url=url,
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self.timeout,
		)
		response_json = json.loads(response.decode("utf-8"))
		content = self._extract_conversation_response(response_json)
		if not content:
			return
		self.start_conversation(image_path, prompt, content)
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
	description = _(
		"""llama.cpp is a state-of-the-art, open-source solution for running large language models locally and in the cloud.
This add-on integration assumes that you have obtained llama.cpp from Github and an image capable model from Huggingface or another repository, and that a server is currently running to handle requests. Though the process for getting this working is largely a task for the user that knows what they are doing, you can find basic steps in the add-on documentation."""
	)

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
		}
		effective_max = kw.get("max_tokens", self.max_tokens)
		if effective_max is not None:
			payload["n_predict"] = effective_max
		if image_data:
			payload["image_data"] = image_data
		return payload

	def _get_conversation_url(self):
		return urllib.parse.urljoin(
			self.base_url or "http://localhost:8080", "completion"
		)

	def _get_conversation_headers(self):
		return {"Content-Type": "application/json"}

	def _extract_conversation_response(self, response_json):
		if "content" not in response_json:
			import ui

			ui.message(
				_(
					"Image recognition response appears to be malformed.\n{response}"
				).format(response=repr(response_json))
			)
			return ""
		return response_json["content"]

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		prompt = kw.get("prompt") or self.prompt
		messages = [{"role": "user", "content": prompt, "image": base64_image}]
		payload = self.build_conversation_payload(
			messages, max_tokens=kw.get("max_tokens", self.max_tokens)
		)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(
			url=url,
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self.timeout,
		)
		response_json = json.loads(response.decode("utf-8"))
		content = self._extract_conversation_response(response_json)
		if not content:
			return
		self.start_conversation(image_path, prompt, content)
		return content


class VivoBlueLMVision(BaseDescriptionService):
	name = "vivo BlueLM Vision (NVDA-CN)"
	description = _(
		"A multimodal model from vivo, accessed via NVDA-CN account. This service is provided by the NVDA Chinese community and requires your nvdacn.com credentials."
	)
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
					vivo_messages.append(
						{
							"role": "user",
							"content": f"data:image/jpeg;base64,{msg['image']}",
							"contentType": "image",
						}
					)
				vivo_messages.append(
					{"role": "user", "content": msg["content"], "contentType": "text"}
				)
			else:  # Assistant messages are straightforward.
				vivo_messages.append(
					{
						"role": "assistant",
						"content": msg["content"],
						"contentType": "text",
					}
				)
		return {
			"model": self.internal_model_name,
			"sessionId": str(uuid.uuid4()),
			"messages": vivo_messages,
			"provider": "vivo",
		}

	def _extract_conversation_response(self, response_json):
		"""
		Extracts content from a successful response or raises an exception for business errors.
		This approach prevents caching of failed API calls.
		"""
		import ui

		if response_json.get("code") != 0:
			error_msg = response_json.get("msg", "Unknown error from vivo API")
			log.warning(
				f"VIVO API returned a business error. Code: {response_json.get('code')}, Message: {error_msg}"
			)
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
			if (
				isinstance(inner_data, list)
				and len(inner_data) > 0
				and "text" in inner_data[0]
			):
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
			params = {"requestId": request_id}
			log.debug(f"Preparing VIVO request with ID: {request_id}")
			# This is the only place that might raise an error without a prior ui.message() call.
			headers = vivo_auth.gen_sign_headers(
				self.nvdacn_user, self.nvdacn_pass, "POST", uri, params
			)
			headers["Content-Type"] = "application/json"
			payload = self.build_conversation_payload(messages)
			full_url = (
				f"https://api-ai.vivo.com.cn{uri}?{urllib.parse.urlencode(params)}"
			)
			log.info(
				f"Sending request to VIVO API endpoint for request ID: {request_id}"
			)
			# The global post() function handles its own UI messaging for network errors and will raise IOError.
			response_bytes = post(
				url=full_url,
				headers=headers,
				data=json.dumps(payload).encode("utf-8"),
				timeout=self.timeout,
			)
			if not response_bytes:
				# This case is a safeguard; post() should raise an exception on failure.
				raise IOError(_("Network request failed unexpectedly."))
			response_json = json.loads(response_bytes.decode("utf-8"))
			# This method also handles its own UI messaging and will raise IOError on VIVO business errors.
			return self._extract_conversation_response(response_json)
		except (ValueError, ConnectionError, json.JSONDecodeError) as e:
			# This includes auth errors from vivo_auth, or malformed JSON responses.
			import ui

			log.error(
				f"An error occurred during VIVO request preparation or parsing: {e}",
				exc_info=True,
			)
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
		prompt = kw.get("prompt") or self.prompt
		messages = [
			{"role": "user", "content": prompt, "image": encode_image(image_path)}
		]
		content = self._perform_vivo_request(messages)
		self.start_conversation(image_path, prompt, content)
		return content

	def add_to_conversation(
		self, user_message, image_path=None, include_original_image=True
	):
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


class Seer(BaseDescriptionService):
	name = "Seer"
	needs_api_key = False
	needs_base_url = True
	# translators: description of the Seer local vision provider
	description = _(
		"Private, on-device image descriptions using PaliGemma2. "
		"No API key or cloud connection required. "
		"Note: this is a captioning model, prompts and follow-up questions are not supported. "
		"Install the Seer daemon to get started."
	)
	about_url = "https://github.com/recursia-lab/Seer"
	supported_formats = [".jpeg", ".jpg", ".png", ".webp", ".bmp"]

	@cached_description
	def process(self, image_path, **kw):
		base64_image = encode_image(image_path)
		payload = json.dumps(
			{
				"image_b64": base64_image,
				"task": "caption",
			}
		).encode("utf-8")
		headers = {"Content-Type": "application/json"}
		url = urllib.parse.urljoin(self.base_url.rstrip("/") + "/", "describe")
		response = post(url=url, headers=headers, data=payload, timeout=self.timeout)
		if not response:
			return None
		resp_json = json.loads(response.decode("utf-8"))
		content = resp_json.get("description", "").strip()
		if not content:
			return None
		return content

	def add_to_conversation(
		self, user_message, image_path=None, include_original_image=True
	):
		# PaliGemma2 is a captioner, not a conversational model
		return _(
			"Seer uses PaliGemma2 which describes images but does not support follow-up questions."
		)


def encode_multipart_formdata(fields, files):
	boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
	body = bytearray()
	for key, value in fields.items():
		if value is None:
			continue
		body.extend(f"--{boundary}\r\n".encode("utf-8"))
		body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"))
		body.extend(f"{value}\r\n".encode("utf-8"))
	for key, (filename, file_bytes, content_type) in files.items():
		body.extend(f"--{boundary}\r\n".encode("utf-8"))
		body.extend(
			f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode("utf-8")
		)
		body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
		body.extend(file_bytes)
		body.extend(b"\r\n")
	body.extend(f"--{boundary}--\r\n".encode("utf-8"))
	content_type_header = f"multipart/form-data; boundary={boundary}"
	return bytes(body), content_type_header


class DatalabChandra2(BaseDescriptionService):
	name = "Datalab Chandra 2"
	# translators: description of the Datalab Chandra 2 vision model
	description = _(
		"Datalab Chandra 2 is a state-of-the-art vision and OCR model specialized in complex document layouts, "
		"tables, forms, handwriting, charts, and math. Supports Datalab's Cloud / On-Prem API as well as "
		"self-hosted OpenAI-compatible vLLM endpoints."
	)
	about_url = "https://github.com/datalab-to/chandra"
	DEFAULT_PROMPT = (
		"Extract and transcribe all text, tables, forms, math formulas, and layout from this image in markdown format. "
		"Describe any visual elements or diagrams."
	)
	needs_api_key = True
	needs_base_url = True
	supported_formats = [".jpeg", ".jpg", ".png", ".webp"]

	@property
	def mode(self):
		return ch.config[self.name].get("mode", "balanced")

	@mode.setter
	def mode(self, value):
		ch.config[self.name]["mode"] = value

	@property
	def internal_model_name(self):
		return self.chosen_model or "datalab-to/chandra-ocr-2"

	def is_convert_api(self):
		url = (self.base_url or "").strip().lower()
		return (
			not url
			or "datalab.to" in url
			or url.endswith("/convert")
			or "/api/v1/convert" in url
		)

	@property
	def is_available(self):
		url = (self.base_url or "").strip().lower()
		if not url or "datalab.to" in url:
			return bool(self.api_key)
		return True

	def _get_conversation_url(self):
		base = (self.base_url or "http://localhost:8000/v1").rstrip("/")
		if base.endswith("/chat/completions"):
			return base
		return f"{base}/chat/completions"

	def _get_conversation_headers(self):
		headers = {"Content-Type": "application/json"}
		if self.api_key:
			headers["Authorization"] = f"Bearer {self.api_key}"
		return headers

	def _process_convert_api(self, image_path, **kw):
		import ui
		import wx

		prompt = kw.get("prompt") or self.prompt
		filename = os.path.basename(image_path)
		ext = os.path.splitext(filename)[1].lower()
		if ext in (".jpg", ".jpeg"):
			mime_type = "image/jpeg"
		elif ext == ".png":
			mime_type = "image/png"
		elif ext == ".webp":
			mime_type = "image/webp"
		else:
			mime_type = "image/png"
			if not filename.endswith(".png"):
				filename += ".png"

		with open(image_path, "rb") as f:
			file_bytes = f.read()

		mode_val = kw.get("mode") or self.mode
		if mode_val not in ("fast", "balanced", "accurate"):
			mode_val = "balanced"
		fields = {
			"output_format": "markdown",
			"mode": mode_val,
			"paginate": "false",
		}
		files = {
			"file": (filename, file_bytes, mime_type),
		}
		data_bytes, content_type_header = encode_multipart_formdata(fields, files)

		convert_url = (kw.get("base_url") or self.base_url or "").strip()
		if not convert_url:
			convert_url = "https://www.datalab.to/api/v1/convert"

		api_key = kw.get("api_key") or self.api_key
		headers = {
			"Content-Type": content_type_header,
			"User-Agent": "NVDA-AIContentDescriber/1.0",
		}
		if api_key:
			headers["X-API-Key"] = api_key

		timeout_val = int(kw.get("timeout") or self.timeout or 100)

		try:
			initial_response = post(
				url=convert_url,
				headers=headers,
				data=data_bytes,
				timeout=min(timeout_val, 30),
			)
		except Exception as e:
			log.exception("Error calling Datalab conversion API")
			# translators: message spoken when an error occurs while contacting the Datalab API
			wx.CallAfter(ui.message, _("Datalab API error: {error}").format(error=str(e)))
			return None

		if not initial_response:
			return None

		try:
			initial_json = json.loads(initial_response.decode("utf-8"))
		except json.JSONDecodeError:
			# translators: message spoken when the Datalab API returns an invalid or non-JSON response
			wx.CallAfter(ui.message, _("Invalid response received from Datalab API."))
			return None

		if not initial_json.get("success", True) or initial_json.get("error"):
			# translators: message spoken when a Datalab conversion request fails
			err = initial_json.get("error") or _("Datalab conversion request failed.")
			wx.CallAfter(ui.message, str(err))
			return None

		request_check_url = initial_json.get("request_check_url")
		if not request_check_url:
			if "markdown" in initial_json and initial_json["markdown"]:
				content = initial_json["markdown"]
				self.start_conversation(image_path, prompt, content)
				return content
			request_id = initial_json.get("request_id")
			if request_id:
				base = convert_url.split("/api/v1/convert")[0] or "https://www.datalab.to"
				request_check_url = f"{base}/api/v1/convert/{request_id}"
			else:
				# translators: message spoken when Datalab does not return a request check URL
				wx.CallAfter(ui.message, _("No request check URL returned by Datalab."))
				return None

		request_check_url = urllib.parse.urljoin(convert_url, request_check_url)

		check_headers = {
			"User-Agent": "NVDA-AIContentDescriber/1.0",
		}
		if api_key:
			check_headers["X-API-Key"] = api_key

		start_time = time.time()
		while time.time() - start_time < timeout_val:
			time.sleep(1)
			req = urllib.request.Request(request_check_url, headers=check_headers, method="GET")
			try:
				with urllib.request.urlopen(req, timeout=10) as resp:
					resp_bytes = resp.read()
			except urllib.error.HTTPError as e:
				if e.code == 429 or e.code >= 500:
					log.debug(f"Retryable polling error from Datalab: {e}")
					continue
				log.error(f"Datalab polling failed: {e}")
				# translators: message spoken when checking the status of a Datalab conversion fails
				wx.CallAfter(ui.message, _("Datalab API error: {error}").format(error=str(e)))
				return None
			except IOError as e:
				log.debug(f"Polling error from Datalab: {e}")
				continue
			except Exception as e:
				log.debug(f"Unexpected error polling Datalab: {e}")
				continue

			try:
				check_json = json.loads(resp_bytes.decode("utf-8"))
			except json.JSONDecodeError:
				continue

			status = str(check_json.get("status", "")).lower()
			if status == "complete":
				if check_json.get("success") is False or (check_json.get("error") and not check_json.get("markdown")):
					# translators: message spoken when Datalab Chandra 2 conversion fails
					err_msg = check_json.get("error") or _("Datalab Chandra 2 conversion failed.")
					wx.CallAfter(ui.message, str(err_msg))
					return None

				markdown = check_json.get("markdown")
				if markdown is None and "result" in check_json and isinstance(check_json["result"], dict):
					markdown = check_json["result"].get("markdown")
				if not markdown:
					markdown = check_json.get("html") or check_json.get("text") or ""
				if not markdown and check_json.get("result_url"):
					result_url = check_json["result_url"]
					try:
						with urllib.request.urlopen(result_url, timeout=15) as r_resp:
							r_json = json.loads(r_resp.read().decode("utf-8"))
							markdown = r_json.get("markdown", "")
					except Exception as e:
						log.debug(f"Failed fetching result_url: {e}")
				if markdown:
					self.start_conversation(image_path, prompt, markdown)
					return markdown
				# translators: message spoken when Datalab Chandra 2 returns an empty response
				wx.CallAfter(ui.message, _("No content returned from Datalab Chandra 2."))
				return None
			elif status in ("failed", "error"):
				# translators: message spoken when Datalab Chandra 2 conversion fails
				err_msg = check_json.get("error") or _("Datalab Chandra 2 conversion failed.")
				wx.CallAfter(ui.message, str(err_msg))
				return None

		# translators: message spoken when Datalab Chandra 2 conversion times out
		wx.CallAfter(ui.message, _("Datalab Chandra 2 conversion timed out."))
		return None

	def _process_openai_api(self, image_path, **kw):
		prompt = kw.get("prompt") or self.prompt
		base64_image = encode_image(image_path)
		messages = [{"role": "user", "content": prompt, "image": base64_image}]
		payload = self.build_conversation_payload(
			messages, max_tokens=kw.get("max_tokens", self.max_tokens)
		)
		headers = self._get_conversation_headers()
		url = self._get_conversation_url()
		response = post(
			url=url,
			headers=headers,
			data=json.dumps(payload).encode("utf-8"),
			timeout=self.timeout,
		)
		if not response:
			return None
		response_json = json.loads(response.decode("utf-8"))
		content = self._extract_conversation_response(response_json)
		if not content:
			return None
		self.start_conversation(image_path, prompt, content)
		return content

	@cached_description
	def process(self, image_path, **kw):
		if self.is_convert_api():
			return self._process_convert_api(image_path, **kw)
		return self._process_openai_api(image_path, **kw)

	def add_to_conversation(
		self, user_message, image_path=None, include_original_image=True
	):
		if self.is_convert_api():
			# translators: message spoken when a user attempts a follow-up question on Datalab Convert API
			return _(
				"Datalab Chandra 2 Convert API is specialized for OCR and document transcription, "
				"and does not support follow-up questions."
			)
		return super().add_to_conversation(
			user_message, image_path=image_path, include_original_image=include_original_image
		)


models = [
	# OpenAI
	GPT4O(),
	GPT41(),
	GPT41Mini(),
	GPT41Nano(),
	O4Mini(),
	O3(),
	O3Mini(),
	O3Pro(),
	GPT5(),
	GPT5Mini(),
	GPT5Nano(),
	GPT5Chat(),
	GPT54(),
	GPT54Mini(),
	GPT54Nano(),
	GPT55(),
	GPT55Pro(),
	GPT4Turbo(),
	# Anthropic
	Claude4_5Sonnet(),
	Claude4_6Sonnet(),
	Claude5Sonnet(),
	Claude4_5Opus(),
	Claude4_6Opus(),
	Claude4_7Opus(),
	Claude4_8Opus(),
	Claude5Opus(),
	Claude5Fable(),
	Claude5_1Fable(),
	# Google
	Gemini2_5Flash(),
	Gemini2_5FlashLite(),
	Gemini2_5Pro(),
	Gemini3FlashPreview(),
	Gemini3_1FlashLitePreview(),
	Gemini3_1ProPreview(),
	Gemini3_5Flash(),
	# xAI
	Grok4FastNonReasoning(),
	Grok4FastReasoning(),
	Grok4(),
	Grok4_3(),
	Grok2Vision(),
	# Mistral
	PixtralLarge(),
	# Moonshot AI (Kimi)
	KimiK3(),
	KimiK2_6(),
	KimiK2_5(),
	# vivo (NVDA-CN)
	VivoBlueLMVision(),
	# Datalab
	DatalabChandra2(),
	# Free
	PollinationsAI(),
	# Local / self-hosted
	Ollama(),
	Seer(),
	LlamaCPP(),
	LiteLLMProxy(),
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

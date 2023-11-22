# Vision API interfaces for the AI Content Describer NVDA add-on
# Copyright (C) 2023, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import base64
import json
import tempfile
import urllib.request

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
	DEFAULT_PROMPT = None
	supported_formats = []

	def process(self):
		pass  # implement in subclasses


class GPT4(BaseDescriptionService):
	name = "GPT-4 vision"
	DEFAULT_PROMPT = "Describe this image succinctly, but in as much detail as possible."
	supported_formats = [
		".gif",
		".jpeg",
		".jpg",
		".png",
		".webp",
	]

	def __init__(self):
		super().__init__()

	def process(self, image_path, **kw):
		prompt = kw.get("prompt", self.DEFAULT_PROMPT)
		max_tokens = kw.get("max_tokens", 250)
		timeout = kw.get("timeout", 15)
		cache_descriptions = kw.get("cache_descriptions", True)
		api_key = kw.get("api_key")
		base64_image = encode_image(image_path)
		# have we seen this image before?
		cache.read_cache()
		description = cache.cache.get(base64_image)
		if description is not None:
			return description
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {api_key}"
		}
		payload = {
			"model": "gpt-4-vision-preview",
			"messages": [
				{
					"role": "user",
					"content": [
						{
							"type": "text",
							"text": prompt
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
			"max_tokens": max_tokens
		}
		response = post(url="https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload).encode('utf-8'), timeout=timeout)
		response = json.loads(response.decode('utf-8'))
		# import test_response
		# response = test_response.response
		content = response["choices"][0]["message"]["content"]
		if not content:
			ui.message("content returned none")
		if content:
			if cache_descriptions:
				cache.read_cache()
				cache.cache[base64_image] = content
				cache.write_cache()
			return content

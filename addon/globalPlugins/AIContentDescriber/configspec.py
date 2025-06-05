# Configuration specification for the AI Content Describer NVDA add-on
# Copyright (C) 2023, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


from io import StringIO


configspec = StringIO("""[GPT-4 vision]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)
# these values are only maintained for backward compatibility and in case a downgrade is necessary
# changing them will do nothing on versions later than 2024.x.x.
# For that, please see the same options under the [global] section.
optimize_for_size = boolean(default=False)
open_in_dialog = boolean(default=False)

[Claude 3.5 Sonnet]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[GPT-4 turbo]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[GPT-4 omni]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Google Gemini pro vision]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Google Gemini 1.5 Flash-8B]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Google Gemini 1.5 Pro]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Google Gemini 2.0 Flash]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Google Gemini 2.0 Flash-Lite Preview]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Ollama]
base_url = string(default="http://localhost:11434")
prompt = string(default="")
chosen_model = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=60, min=1)

[llama.cpp]
base_url = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=60, min=1)

[Pixtral Large]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Claude 3 Haiku]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Claude 3 Sonnet]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Claude 3 Opus]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Pollinations (OpenAI)]
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[global]
optimize_for_size = boolean(default=False)
open_in_dialog = boolean(default=True)
last_used_model = string(default="Pollinations (OpenAI)")
""")

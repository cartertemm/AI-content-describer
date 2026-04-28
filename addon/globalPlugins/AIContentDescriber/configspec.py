# Configuration specification for the AI Content Describer NVDA add-on
# Copyright (C) 2023, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


from io import StringIO


configspec = StringIO("""[Claude 4.6 Opus]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[Claude 4.6 Sonnet]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=20, min=1)

[Claude 4.5 Opus]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[Claude 4.5 Sonnet]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=20, min=1)

[Claude 4.5 Haiku]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Claude 4.1 Opus]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

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

[Google Gemini 2.5 Flash]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=2048)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Google Gemini 2.5 Flash-Lite]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Google Gemini 2.5 Pro]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=2048)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Google Gemini 3 Flash Preview]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=2048)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Google Gemini 3.1 Flash-Lite Preview]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Google Gemini 3.1 Pro Preview]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=2048)
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

[Pollinations (OpenAI)]
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[OpenAI O3]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[OpenAI O3 pro]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[OpenAI O3 mini]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=20, min=1)

[OpenAI O4 mini]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[GPT-4.1]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[GPT-4.1 mini]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=20, min=1)

[GPT-4.1 nano]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[GPT-5]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[GPT-5 mini]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=20, min=1)

[GPT-5 nano]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[GPT-5 chat]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[GPT-5.4]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[GPT-5.4 mini]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=20, min=1)

[GPT-5.4 nano]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)

[Grok 2 vision]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[Grok 4]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[Grok 4 Fast (reasoning)]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[Grok 4 Fast (non-reasoning)]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=15, min=1)


[Claude 4 Opus]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[Claude 4 Sonnet]
api_key = string(default="")
prompt = string(default="")
max_tokens = integer(default=300)
cache_descriptions = boolean(default=False)
timeout = integer(default=20, min=1)

[vivo BlueLM Vision (NVDA-CN)]
nvdacn_user = string(default="")
nvdacn_pass = string(default="")
prompt = string(default="")
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[LiteLLM Proxy]
base_url = string(default="")
api_key = string(default="")
chosen_model = string(default="")
prompt = string(default="")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=30, min=1)

[global]
optimize_for_size = boolean(default=False)
open_in_dialog = boolean(default=True)
last_used_model = string(default="Pollinations (OpenAI)")
""")

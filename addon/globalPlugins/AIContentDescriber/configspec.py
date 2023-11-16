from io import StringIO


configspec = StringIO("""[GPT-4 vision]
api_key = string(default="")
prompt = string(default="Describe this image succinctly, but in as much detail as possible.")
max_tokens = integer(default=250)
cache_descriptions = boolean(default=False)
timeout = integer(default=10, min=1)
optimize_for_size = boolean(default=False)
open_in_dialog = boolean(default=False)
""")

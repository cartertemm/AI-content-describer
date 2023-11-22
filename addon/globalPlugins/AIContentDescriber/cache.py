# Simple JSON-based cache for the AI Content Describer NVDA add-on
# Copyright (C) 2023, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import os
import json
import globalVars


CACHE_FILE = "images.cache"
CACHE_PATH = os.path.abspath(os.path.join(globalVars.appArgs.configPath, CACHE_FILE))
cache = {}


def create_cache():
	global cache
	cache = {}
	write_cache()  # create the file


def read_cache():
	global cache
	if not os.path.isfile(CACHE_PATH):
		create_cache()
		return
	try:
		with open(CACHE_PATH, "r") as f:
			cache = json.load(f)
	except json.decoder.JSONDecodeError:  #  todo: try to fix corrupt files before trashing them
		create_cache()


def write_cache():
	with open(CACHE_PATH, "w") as f:
		json.dump(cache, f, indent="\t")

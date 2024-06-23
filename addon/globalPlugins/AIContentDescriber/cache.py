# Simple JSON-based cache for the AI Content Describer NVDA add-on
# Copyright (C) 2023, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import os
import json
import globalVars

cache = {}

def _get_cache_path(cache_name):
	return os.path.abspath(os.path.join(globalVars.appArgs.configPath, cache_name + ".cache"))

def create_cache(cache_name):
	global cache
	cache[cache_name]= {}
	write_cache(cache_name)  # create the file


def read_cache(cache_name):
	global cache
	cache_path = _get_cache_path(cache_name)
	if not os.path.isfile(cache_path):
		create_cache(cache_name)
		return
	try:
		with open(cache_path, "r") as f:
			cache[cache_name] = json.load(f)
	except json.decoder.JSONDecodeError:  #  todo: try to fix corrupt files before trashing them
		create_cache(cache_name)


def write_cache(cache_name):
	cache_path = _get_cache_path(cache_name)
	with open(cache_path, "w") as f:
		json.dump(cache[cache_name], f, indent="\t")

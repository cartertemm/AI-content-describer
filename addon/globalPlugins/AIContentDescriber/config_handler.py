# Configuration handling for the AI Content Describer NVDA add-on
# Copyright (C) 2023 - 2026, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import os
import logging
from configobj import ConfigObj, ConfigObjError, flatten_errors
from configobj.validate import Validator
from configspec import configspec
import globalVars


log = logging.getLogger(__name__)
config = None


def get_config_path():
	return os.path.abspath(os.path.join(globalVars.appArgs.configPath, "AIContentDescriber.conf"))


def get_unused_backup_path():
	"""Returns a backup path that does not exist yet, so that an earlier backup is never overwritten."""
	path = get_config_path() + ".bak"
	number = 1
	while os.path.exists(path):
		number += 1
		path = get_config_path() + ".bak%d" % number
	return path


def _read_config(path):
	# seek back to the beginning of the spec for every read, in case this is called twice
	configspec.seek(0)
	return ConfigObj(
		infile=path, configspec=configspec, default_encoding="UTF8", create_empty=True
	)


def load_config():
	"""Loads the add-on's configuration.

	A file that cannot be parsed is moved to a backup path and replaced with defaults.
	Returns a (parse error description, backup path) tuple when that happens, None otherwise.
	"""
	global config
	path = get_config_path()
	failure = None
	try:
		config = _read_config(path)
	except ConfigObjError as e:
		log.exception("While loading the configuration file")
		failure = (str(e), get_unused_backup_path())
		os.rename(path, failure[1])
		config = _read_config(path)
	validator = Validator()
	result = config.validate(validator, copy=True)
	if result is not True:
		errors = report_validation_errors(config, result)
		errors = "\n".join(errors)
		e = "error" + ("" if len(errors) == 1 else "s")
		log.error(e+ " were encountered while validating the configuration.\n" + errors)
	return failure


def report_validation_errors(config, validation_result):
	"""Return any errors that were detected with the configuration file to display a friendly message."""
	errors = []
	for (section_list, key, _) in flatten_errors(config, validation_result):
		if key:
			errors.append(
				'"%s" key in section "%s" failed validation'
				% (key, ", ".join(section_list))
			)
		else:
			errors.append('missing required section "%s"' % (", ".join(section_list)))
	return errors


def migrate_config_if_needed():
	"""Fixes any issues with the user's config that may still be present after a version upgrade.

	It is important that we take extra care *not* to remove any settings
	from the configspec, as this will error out and require manual
	alteration.

	Returns True if a migration took place, False otherwise.
	"""
	needs_migration = os.path.isfile(os.path.abspath(os.path.join(globalVars.appArgs.configPath, "AIContentDescriber_config_migration")))
	if not needs_migration:
		return
	# we used to (rather stupidly) store all the settings under the GPT-4 vision model
	## as this was the first and only one to have been implemented for a while
	migrated = False
	old_settings_section = "GPT-4 vision"
	new_settings_section = "global"
	old_gpt_settings = ["optimize_for_size", "open_in_dialog"]
	if old_settings_section not in config:
		os.remove(os.path.abspath(os.path.join(globalVars.appArgs.configPath, "AIContentDescriber_config_migration")))
		return False
	validator = Validator()
	for setting in old_gpt_settings:
		value = config[old_settings_section].get(setting)
		if value is not None:
			# the old section is absent from the configspec, so its values are still raw strings
			value = validator.check("boolean", value)
		new_value = config[new_settings_section].get(setting)
		if value is not None and value != new_value:
			if not migrated:
				migrated = True
			# port it over
			config["global"][setting] = value
			del config[old_settings_section][setting]
	os.remove(os.path.abspath(os.path.join(globalVars.appArgs.configPath, "AIContentDescriber_config_migration")))
	return migrated

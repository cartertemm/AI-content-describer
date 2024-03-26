# Configuration handling for the AI Content Describer NVDA add-on
# Copyright (C) 2023, Carter Temm
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


def load_config():
	"""Loads the add-on's configuration."""
	global config
	path = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "AIContentDescriber.conf"))
	# seek back to the beginning of the spec for every read, in case this is called twice
	configspec.seek(0)
	try:
		config = ConfigObj(
			infile=path, configspec=configspec, encoding="UTF8", create_empty=True
		)
	except ConfigObjError as exc:
		log.exception("While loading the configuration file")
		return
	validator = Validator()
	result = config.validate(validator, copy=True)
	if result != True:
		errors = report_validation_errors(config, result)
		errors = "\n".join(errors)
		e = "error" + ("" if len(errors) == 1 else "s")
		log.error(e+ " were encountered while validating the configuration.\n" + errors)


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
	for setting in old_gpt_settings:
		value = config[old_settings_section].get(setting)
		new_value = config[new_settings_section].get(setting)
		if value is not None and value != new_value:
			if not migrated:
				migrated = True
			# port it over
			config["global"][setting] = value
			del config[old_settings_section][setting]
	os.remove(os.path.abspath(os.path.join(globalVars.appArgs.configPath, "AIContentDescriber_config_migration")))
	return migrated

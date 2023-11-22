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

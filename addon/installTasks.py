# Tasks to perform during installation of the AI Content Describer NVDA add-on
# Copyright (C) 2023 - 2026, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import os
import shutil
import sys
import wx
import addonHandler
import globalVars
import gui
addonHandler.initTranslation()


def onInstall():
	for addon in addonHandler.getAvailableAddons():
		if addon.name == "AI Content Describer":
			# Translators: The message displayed if during installation, there is an incompatable version already installed
			msg = _("There appears to be an older version of this add-on installed that is incompatable with future versions because the name has changed. It will be removed the next time NVDA is restarted.")
			# Translators: The title of the message dialog when the user is installing the add-on
			title = _("AI Content Describer")
			gui.messageBox(msg, title, wx.OK)
			addon.requestRemove()
			#addonGui.promptUserForRestart()
			continue
	# This file is placed into the root of the NVDA configuration directory to signify that a config migration may be needed
	with open(os.path.abspath(os.path.join(globalVars.appArgs.configPath, "AIContentDescriber_config_migration")), "w") as f:
		f.write("File generated automatically on installation or update of the AI content describer addon. If you are reading this, you are probably good to delete it.")


def onUninstall():
	py_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
	deps_path = os.path.abspath(os.path.join(globalVars.appArgs.configPath, f"aic-py-{py_ver}"))
	if os.path.isdir(deps_path):
		shutil.rmtree(deps_path, ignore_errors=True)

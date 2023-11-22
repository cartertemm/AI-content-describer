# Tasks to perform during installation of the AI Content Describer NVDA add-on
# Copyright (C) 2023, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import wx
import addonHandler
import gui
from gui import addonGui
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

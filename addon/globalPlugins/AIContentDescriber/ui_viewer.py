# *-* coding: utf-8 *-*

# NVDA Add-on: AI Content Describer
# Copyright (C) 2023 - 2026, Carter Temm
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import os
import tempfile
import threading
import logging
log = logging.getLogger(__name__)

import addonHandler
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Couldn't initialise translations. Is this addon running from NVDA's scratchpad directory?")

import wx
import ui
import tones
import dependency_checker
dependency_checker.expand_path()
from PIL import ImageGrab


CC_MAX_TOKENS = 16384
PROMPT = """You are given a screenshot of a Windows desktop or application. Reconstruct all visible UI controls as semantic, accessible HTML. Follow these rules exactly:

1. Map every visible control to the correct HTML element:
	- Buttons -> <button>
	- Checkboxes -> <input type="checkbox">
	- Radio buttons -> <input type="radio">
	- Single-line text fields -> <input type="text">
	- Multi-line text areas -> <textarea>
	- Dropdowns and combo boxes -> <select> with <option> elements for each visible choice
	- Sliders -> <input type="range">
	- Links -> <a>
	- Static labels and hint or description text -> <label> or <p>
	- Group boxes and panels -> <fieldset> with <legend>
	- Tabs -> <button role="tab">
	- List views and tree views -> <ul> or <ol> with appropriate role attributes
	- Progress bars -> <progress>
	- Spin boxes and number fields -> <input type="number">

2. Preserve all text exactly as shown. Do not rephrase, reorder, summarize, or omit any text under any circumstances.

3. Associate visible labels with their controls using <label for="..."> and matching id attributes.

4. For any control with no visible label, infer an appropriate label based on its position, context, and nearby elements. These inferred labels must be listed below the header at the bottom of the output.

5. Ignore any NVDA windows or AI Content Describer windows visible on screen.

6. Output the following, in this order:
	First, the full HTML reconstruction of the screen contents, in reading order (top to bottom, left to right).
	If you inferred or changed labels:
		Add a <h1> element at the very bottom of the output:
		<h1>Changes</h1>
		<ul>
		<li>Unlabelled control {position description, e.g. "top-left button"}, set to {inferred label}</li>
		</ul>
		</h1>
	If no labels were inferred, do not include the <h1> element with an empty <ul></ul>.

7. Do not reproduce visual styles, colors, fonts, or decorative elements. Only structure and content matter.

8. Never modify, summarize, or omit any text content. If a button says "Don't show this again", output exactly "Don't show this again".

9. Include all hint text, tooltips, descriptions, and supplementary text visible near controls."""


def _process(service, file):
	tones.beep(300, 200)
	# Translators: message spoken when fetching a UI description
	wx.CallAfter(ui.message, _("Retrieving UI description using {name}...").format(name=service.name))
	try:
		result = service.process(file, prompt=PROMPT, max_tokens=CC_MAX_TOKENS, cache_descriptions=False)
		if result:
			# Translators: title of the browseable message showing reconstructed UI controls
			wx.CallAfter(ui.browseableMessage, result, _("UI Controls"), True, sanitizeHtmlFunc=lambda html:html)
	finally:
		log.debug("Cleaning up image: " + file)
		os.unlink(file)


def describe_ui(plugin, service):
	if plugin.is_screen_curtain_running():
		# Translators: message spoken when the screen curtain is active and the user attempts to describe the UI
		ui.message(_("Please disable windows screen curtain before using AI content describer."))
		return
	if not service or not service.is_available:
		# Translators: message spoken when no service is available for UI description
		ui.message(_("To describe content, you must provide an API key or base URL in the AI image describer category of the NVDA settings dialog. Please consult add-on help for more information"))
		return
	snap = ImageGrab.grab()
	if not snap:
		# Translators: message spoken when capturing the screen fails
		ui.message(_("Could not get window content"))
		return
	file = tempfile.mktemp(suffix=".png")
	snap.save(file)
	threading.Thread(target=_process, args=(service, file)).start()

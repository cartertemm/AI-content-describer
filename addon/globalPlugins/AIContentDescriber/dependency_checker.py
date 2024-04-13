import sys
import os
import glob
import threading
import urllib.error
import urllib.request
import zipfile
import wx

import addonHandler
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Couldn't initialise translations. Is this addon running from NVDA's scratchpad directory?")
import core
import gui
import globalVars


class DownloadProgressDialog(wx.Dialog):
	def __init__(self, parent, title, url):
		super().__init__(parent, title=title, size=(400, 100))
		self.url = url
		self.download = None
		self.download_canceled = False
		self.error = None
		self.gauge = wx.Gauge(self, range=100)
		self.gauge.SetValue(0)
		self.button = wx.Button(self, label='Cancel')
		self.button.Bind(wx.EVT_BUTTON, self.OnCancel)
		self.Bind(wx.EVT_CLOSE, self.OnCancel)
		message = wx.StaticText(self, label="Downloading dependencies, please wait...")
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.gauge, 0, wx.EXPAND)
		sizer.Add(self.button, 0, wx.EXPAND)
		sizer.Add(message, 0, wx.ALIGN_CENTER)
		self.SetSizerAndFit(sizer)

	def start_download(self):
		self.download_thread = threading.Thread(target=self._start_download, daemon=True)
		self.download_thread.start()

	def _start_download(self):
		try:
			self.download = urllib.request.urlretrieve(self.url, reporthook=self.OnProgress)
		except urllib.error.URLError as error:
			print(error.response)
			self.error = error
			wx.CallAfter(self.EndModal, wx.ID_ABORT)
			return False
		except Exception as error:
			print(error)
			self.error = error
			wx.CallAfter(self.EndModal, wx.ID_ABORT)
			return False
		wx.CallAfter(self.EndModal, wx.ID_OK)

	def OnProgress(self, count, blocksize, totalsize):
		if self.download_canceled:
			wx.CallAfter(self.EndModal, wx.ID_CANCEL)
			raise Exception("Dependency download canceled.")
		so_far = count * blocksize
		percent = so_far * 100 / totalsize
		percent = round(percent)
		wx.CallAfter(self.gauge.SetValue, percent)
		return True

	def OnCancel(self, event):
		self.download_canceled = True
		wx.CallAfter(self.EndModal, wx.ID_CANCEL)


def show_modal(dlg):
	gui.mainFrame.prePopup()
	result = dlg.ShowModal()
	gui.mainFrame.postPopup()
	dlg.Destroy()
	return  result


def show_question(parent, title, message):
	dlg = wx.MessageDialog(parent, message, title, wx.YES_NO | wx.ICON_QUESTION)
	result = show_modal(dlg)
	return result == wx.ID_YES


def show_error(parent, title, message):
	dlg = wx.MessageDialog(parent, message, title, style=wx.OK | wx.ICON_ERROR)
	result =  show_modal(dlg)
	return result


def show_information(parent, title, message):
	dlg = wx.MessageDialog(parent, message, title, style=wx.OK | wx.ICON_INFORMATION)
	result =  show_modal(dlg)
	return result


def  prompt_not_found():
	return show_question(
		None,
		# Translators: Summary for this add-on
		_("AI Content Describer"),
		# Translators: the message shown when required dependencies were not found
		_("Some of the dependencies required for this NVDA add-on to run are not available on your computer. Would you like to download them now? NVDA will need to be restarted when this process completes."),
	)


def  prompt_replacement():
	return show_question(
		None,
		# Translators: Summary for this add-on
		_("AI Content Describer"),
		# Translators: the message shown when the wrong dependency versions were found
		_("Some of the dependencies required for this NVDA add-on to run are outdated. Would you like to try to install them now? NVDA will need to be restarted when complete."),
	)


def prompt_deletion():
	return show_question(
		None,
		# Translators: Summary for this add-on
		_("AI Content Describer"),
		# Translators: the message shown when the addon has successfully retrieved the new dependencies, asking the user whether they would like to delete the old ones
		_("Would you like to delete the old dependencies from the configuration? This question will be asked once. If you are running multiple versions of NVDA interchangeably, select no."),
	)


def prompt_restart():
	show_information(
		None,
		# Translators: Summary for this add-on
		_("AI Content Describer"),
		# Translators: Message shown when NVDA is about to restart after the dependencies have been downloaded.
		_("The dependencies have been downloaded successfully. NVDA will now restart for the changes to take affect")
	)
	core.restart()


def dependencies_not_available():
	return show_error(
		None,
		# Translators: Summary for this add-on
		_("AI Content Describer"),
		# Translators: Message displayed when there isn't yet libraries to support the running version of NVDA.
		_("Unfortunately, there doesn't yet seem to be dependencies available for the running version of NVDA. Please submit an issue in our bug tracker or contact the developers. In the meantime, you may wish to disable the add-on to  surpress this  message on startup.")
	)


def download_failed(error):
	return show_error(
		None,
		# Translators: Summary for this add-on
		_("AI Content Describer"),
		# Translators: Message shown when dependencies fail to download.
		_("Unfortunately, there was a problem downloading the dependencies required to run this add-on. Please consult the NVDA log for more details. "+str(error)),
	)


def check_url(url):
	try:
		req = urllib.request.Request(url, method='HEAD')
		with urllib.request.urlopen(req) as response:
			status_code = response.getcode()
			content_length = int(response.headers.get('Content-Length', 0))
			return status_code == 200 and content_length > 0
	except urllib.error.URLError as e:
		print(f"Error: {e.reason}")
		return False


def get_dependencies_path():
	base = globalVars.appArgs.configPath
	py_version_string = sys.version_info
	py_version_string = f"{py_version_string.major}.{py_version_string.minor}"
	path = os.path.abspath(os.path.join(base, f"aic-py-{py_version_string}"))
	return path


def get_dependencies_url():
	return f"https://github.com/cartertemm/AI-content-describer/releases/download/libs-release/aic-py-{sys.version_info.major}.{sys.version_info.minor}.zip"


def  get_all_dependencies():
	base = globalVars.appArgs.configPath
	wildcard= os.path.abspath(os.path.join(base, f"aic-py-*"))
	return glob.glob(wildcard, recursive=False)


def unzip_and_move_dependencies(downloaded_file, destination):
	if not  os.path.isdir(destination):
		os.mkdir(destination)
	with zipfile.ZipFile(downloaded_file, "r") as zf:
		zf.extractall(destination)
	return True


def expand_path():
	sys.path.append(get_dependencies_path())


def collapse_path():
	sys.path.remove(get_dependencies_path())


def check_versions():
	dependencies = get_dependencies_path()
	if os.path.isdir(dependencies) and len(os.listdir(dependencies)) > 0:
		return True
	if prompt_not_found():
		url = get_dependencies_url()
		if not check_url(url):
			dependencies_not_available()
			return False
		dlg = DownloadProgressDialog(
			None,
			# Translators: Summary for this add-on
			_("AI Content Describer"),
			url
		)
		dlg.start_download()
		result = show_modal(dlg)
		if result == wx.ID_OK:
			if dlg.download_canceled:
				return False
			result = unzip_and_move_dependencies(dlg.download[0], globalVars.appArgs.configPath)
			if result:
				os.remove(dlg.download[0])
				prompt_restart()
		elif result == wx.ID_ABORT:
			download_failed(dlg.error)
			return False


wx.CallAfter(check_versions)

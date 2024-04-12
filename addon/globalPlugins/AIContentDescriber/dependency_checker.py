import threading
import urllib.error
import urllib.request
import wx


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
		self.download_thread = threading.Thread(target=self._start_download)
		self.download_thread.start()

	def _start_download(self):
		try:
			self.download = urllib.request.urlretrieve(self.url, reporthook=self.OnProgress)
		except urllib.error.URLError as error:
			print(error.response)
			self.error = error
			self.EndModal(wx.ID_ABORT)
			return False
		except Exception as error:
			print(error)
			self.error = error
			self.EndModal(wx.ID_ABORT)
			return False

	def OnProgress(self, count, blocksize, totalsize):
		if self.download_canceled:
			raise	Exception("Download canceled")
			return False
		so_far = count * blocksize
		percent = so_far * 100 / totalsize
		percent = round(percent)
		print(percent)  # test
		self.gauge.SetValue(percent)
		if so_far >= totalsize:
			self.EndModal(wx.ID_OK)

	def OnCancel(self, event):
		self.download_canceled = True
		self.EndModal(wx.ID_CANCEL)


def show_question(parent, title, message):
	dlg = wx.MessageDialog(parent, message, title, wx.YES_NO | wx.ICON_QUESTION)
	result = dlg.ShowModal()
	dlg.Destroy()
	return result == wx.ID_YES


if __name__ == "__main__":  # test
	ap = wx.App()
	question = show_question(None, "AI content describer", "This NVDA add-on requires libraries that were not found on your computer, and can not work otherwise. Do you want to install them?")
	if question:
		dlg = DownloadProgressDialog(None, "Downloading...", "https://github.com/cartertemm/AI-content-describer/releases/download/v2023.03.29/AIContentDescriber-2024.03.29.nvda-addon")
		dlg.start_download()
		status = dlg.ShowModal()
		if status == wx.ID_OK:
			print("Downloaded to", dlg.download)
		elif status == wx.ID_ABORT:
			print("The download failed.")
		else:
			print("Download cancelled.")

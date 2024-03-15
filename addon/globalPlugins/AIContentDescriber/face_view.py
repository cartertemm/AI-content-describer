import ui
import gui
from gui import settingsDialogs
from gui import guiHelper

import wx
import cv2
from pygrabber import dshow_graph
from logHandler import log


class DeviceChooser(settingsDialogs.SettingsDialog):
	# translators: the title for the dialog that selects the camera
	title = _("Choose a camera")
	helpId = "CameraSelection"

	def postInit(self):
		self.device_list.SetSelection(0)
		self.device_list.SetFocus()

	def makeSettings(self, settingsSizer):
		sizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# translators: the label for the available cameras combo box
		label = _("&Available cameras")
		self.device_list = sizerHelper.addLabeledControl(label, wx.Choice, choices=fd.devices)

	def onOk(self, event):
		fd.chosen_camera = fd.devices[self.device_list.GetSelection()]
		super().onOk(event)

	def onCancel(self, event):
		fd.chosen_camera = None
		super().onCancel(event)


class FaceDetectionInterface:
	def __init__(self):
		self.video_capture = None
		self.devices = []
		self.chosen_camera = None

	def get_direction_percentages(self, frame, face):
		frame_width = frame.shape[1]
		frame_height = frame.shape[0]
		frame_center = (frame_width // 2, frame_height // 2)
		x, y, w, h = face
		face_center = (x + w//2, y + h//2)
		x_center, y_center = frame_center
		x_face, y_face = face_center
		# flip the coordinate placements from RTL to LTR - it makes more sense this way
		x_percent = 100 - int(round((x_face / frame_width) * 100, 0))
		y_percent = 100 - int(round((y_face / frame_height) * 100, 0))
		return x_percent, y_percent

	def get_direction(self, frame, face):
		x_percent, y_percent = self.get_direction_percentages(frame, face)
		#print(f"x: {x_percent}%, y: {y_percent}%")
		directions = []
		if x_percent < 10:
			directions.append("far to the left of ")
		elif x_percent < 30:
			directions.append("to the left of ")
		elif x_percent < 45:
			directions.append("slightly to the left of ")
		elif x_percent > 55:
			directions.append("slightly to the right of ")
		elif x_percent > 70:
				directions.append("to the right of ")
		elif x_percent > 90:
			directions.append("far to the right of ")
		if y_percent < 10:
			directions.append("far below")
		elif y_percent < 30:
			directions.append("below")
		elif y_percent < 45:
			directions.append("slightly below")
		elif y_percent > 55:
			directions.append("slightly above")
		elif y_percent > 70:
			directions.append("above")
		elif y_percent > 90:
			directions.append("far above")
		#print(x_face, x_center)
		return ' and '.join(directions)+" the center" if directions else "face clearly in view"

	def process_frame(self):
		ret, frame = self.video_capture.read()
		ui.message(frame)  # to see what happens when covered up - curious minds do wonder
		if not ret:
			# translators: the message spoken when footage could not be captured from the camera during facial detection
			ui.message(_("Failed to interface with the camera. Please ensure it is not in use by another application, then try again."))
			return
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.1, 6, minSize=(50, 50))
		if len(faces) == 0:
			# translators: the message spoken when there was no face found in the frame
			ui.message(_("No face detected. Please ensure your face is in the frame and that your camera is not covered up."))
		elif len(faces) > 1:
			ui.message(_(f"{faces} detected near the frame."))
		else:
			for face in faces:
				direction = get_direction(frame, face)
				ui.message(direction)
				return direction  # discard the results of the other faces, for now

	def read_frame(self):
		return self.video_capture.read()

	def show_device_dialog(self):
		gui.mainFrame.popupSettingsDialog(DeviceChooser)

	def show_device_dialog_if_needed(self):
		self.devices = get_device_list()
		if len(self.devices) == 0:
			# translators: the message that gets spoken when facial detection cannot find any cameras
			ui.message(_("No camera found on your system. Please connect one and try again."))
			return
		# have we already been successfully using a device?
		if self.chosen_camera is not None and self.chosen_camera in self.devices:
			return  # continue using it
		if len(self.devices) == 1:
			if self.chosen_camera is not None and not self.chosen_camera in self.devices:
				# translators: message spoken when the camera that was being used before has disconnected
				ui.message(_(self.chosen_camera+" is no longer available. Switching to the other on the system."))
			self.chosen_camera = self.devices[0]  # just use the first available
		else:
			self.show_device_dialog()
			return True  # we did need to show it after all

	def run(self, process=True):
		if len(self.devices) == 0:
			# translators: the message that gets spoken when facial detection cannot find any cameras
			ui.message(_("No camera found on your system. Please connect one and try again."))
			return
		dlg_shown = self.show_device_dialog_if_needed()
		if dlg_shown == True:
			self.destroy()  # release the old capture object (if one exists)
			# translators: the message spoken to prompt the user to trigger the command again, after the camera has been chosen
			## annoying behavior, this is a limitation of the way we're doing the UI. Yay for rapid prototyping!
			ui.message(_("Camera selected. You may now trigger the command again."))
			return 
		log.warning(self.chosen_camera)
		try:
			index = self.devices.index(self.chosen_camera)
		except ValueError:  # unlikely: the camera became unavailable between when the user selected it and us triggering the command again.
			if self.show_device_dialog_if_needed():
				# translators: message spoken when the camera becomes unavailable between the user selecting it and triggering it again
				ui.message(_("Camera unavailable. Please try selecting another"))
				return
		if self.video_capture is None:
			self.video_capture = cv2.VideoCapture(index)
		if not self.video_capture.isOpened():
			# translators: message spoken when we could not interface with the chosen camera
			ui.message(_("Failed to interface with the chosen camera"))
			return
		if process:
			self.process_frame()

	def destroy(self):
		if self.video_capture is not None:
			self.video_capture.release()
		self.video_capture = None

	def __del__(self):
		self.destroy()


def get_device_list():
	fg = dshow_graph.FilterGraph()
	try:
		return fg.get_input_devices()
	except Exception as exc:
		log.warning(repr(exc))
		return []


fd = FaceDetectionInterface()

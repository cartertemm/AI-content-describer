import ui
import cv2
from pygrabber import dshow_graph
from logHandler import log


class FaceDetectionInterface:
	def __init__(self):
		self.video_capture = None

	def get_direction(self, frame, face, callback=None):
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
		ui.message(frame)  # to see what happens when covered up
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

	def run(self):
		detected_devices = get_device_list()
		if len(detected_devices) == 0:
			# translators: the message that gets spoken when facial detection cannot find any cameras
			ui.message(_("No camera found on your system. Please connect one and try again."))
			return
		index = 0
		if self.video_capture is None:
			self.video_capture = cv2.VideoCapture(index)
		self.process_frame()

	def destroy(self):
		self.video_capture.release()

	def __del__(self):
		self.destroy()


def get_device_list():
	fg = dshow_graph.FilterGraph()
	try:
		return fg.get_input_devices()
	except Exception as exc:
		log.warning(repr(exc))
		return []

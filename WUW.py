#!/usr/bin/python
from gi.repository import Gtk as gtk
from Marker import *
from ThreadCapture import *

class WUW:

	def __init__(self):
		interface = gtk.Builder()
		interface.add_from_file('wuw.glade')

		self.windows = interface.get_object("WUW")
		interface.connect_signals(self)

		self.displayPictureBox = interface.get_object("displayPictureBox")

		self.initComponent()

        # http://askubuntu.com/questions/328836/glade-quickly-and-changing-an-image-with-code

		img = gtk.Image()
		img.show()
		self.displayPictureBox.add(img)
		self.ThreadCapture = ThreadCapture(img)
		self.displayPictureBox.show()


	def initComponent(self):
		self.YELLOW = 50
		self.GREEN = 135
		self.BLUE = 200
		self.RED = 350

		self.RGB = [[0, 255, 255], [0, 255, 0], [255, 0, 0], [0, 0, 255]]


	def on_mainWindow_destroy(self, widget):
		gtk.main_quit()


	def testMarkers(self, color):
		img = cv2.imread("sample.png")

		hue = color // 2

		lower_range = np.array([max(0, hue - 5), 0, 0], dtype=np.uint8)
		upper_range = np.array([min(180, hue + 5), 255, 255], dtype=np.uint8)

		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		mask = cv2.inRange(img_hsv, lower_range, upper_range)

		binary_img = cv2.bitwise_and(img_hsv, img_hsv, mask=mask)
		binary_img = cv2.cvtColor(binary_img, cv2.COLOR_BGR2GRAY)
		_, binary_img = cv2.threshold(binary_img, 127, 255, cv2.THRESH_BINARY)

		cv2.imshow('sample', binary_img)
		cv2.waitKey(0)


	def drawCameraMarkers(self):
		yellow_marker = Marker(self.YELLOW)
		green_marker = Marker(self.GREEN)
		blue_marker = Marker(self.BLUE)
		red_marker = Marker(self.RED)

		marker_detector = MarkersDetector([yellow_marker, green_marker, blue_marker, red_marker])

		cap = cv2.VideoCapture(0)
		start = time.time()

		while 1:
			_, frame = cap.read()

			m = marker_detector.detect(frame)

			for i, (a, b) in enumerate(m):
				if a != -1:
					cv2.circle(frame, (int(a*4), int(b*4)), 30, RGB[i], thickness=3)

			cv2.imshow("frame", frame)
			set_from_image(gdk_image, mask)
			cv2.waitKey(1)


if __name__ == "__main__":
	wuw = WUW()
	gtk.main()
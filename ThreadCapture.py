import urllib
import gobject
import threading
from Marker import *

class ThreadCapture(threading.Thread):
	'''
	A background thread that takes the MJPEG stream and
	updates the GTK image.
	'''
	def __init__(self, widget):
		super(ThreadCapture, self).__init__()
		self.widget = widget
		self.quit = False

	def get_raw_frame(self):
		'''
		Parse an MJPEG http stream and yield each frame.
		Source: http://stackoverflow.com/a/21844162
		:return: generator of JPEG images
		'''
		cap = cv2.VideoCapture(0)
		start = time.time()

		while 1:
			_, frame = cap.read()
			yield frame
			#cv2.imshow("frame", frame)
			#cv2.waitKey(1)

	def run(self):
		for frame in self.get_raw_frame():
			if self.quit or frame is None:
				return
			loader = gtk.gdk.PixbufLoader('jpeg')
			loader.write(frame)
			loader.close()
			pixbuf = loader.get_pixbuf()
			# Schedule image update to happen in main thread
			gobject.idle_add(self.widget.set_from_pixbuf, pixbuf)
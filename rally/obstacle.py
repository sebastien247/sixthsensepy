import wx


class obstacle:
	def __init__(self, image, x):
		self.image = image
		self.x = x
		self.y = -12
		self.obs_img = None

	def descendre (self, pixels):
		self.y = self.y + pixels


	def afficher(self, BoxRally):
		if not self.obs_img:
			self.obs_img=wx.StaticBitmap(BoxRally , -1, self.image, (self.x, self.y))
		else:
			self.obs_img.SetPosition(wx.Point(self.x, self.y))

	def __del__(self):
		print "dans le destructeur"

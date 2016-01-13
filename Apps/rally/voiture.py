

import wx


class voiture:
	def __init__(self, image):
		self.image = image
		self.x = 150
		self.y = 150
		self.car_img = None

	def gauche (self, pixels):
		self.x = self.x + pixels


	def droite (self, pixels):
		self.x = self.x - pixels

	def afficher(self, BoxRally):
		if not self.car_img:
			self.car_img=wx.StaticBitmap(BoxRally , -1, self.image, (self.x, self.y))
		else:
			self.car_img.SetPosition(wx.Point(self.x, self.y))

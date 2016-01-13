from Apps.rally.obstacle import *
import random

class Mgr_Obstacle:
	def __init__(self, bmp2, BoxRally, heigth, width):
		self.liste = []
		self.BoxRally = BoxRally
		self.bmp2 = bmp2
		self.heigth = heigth
		self.width = width
		self.pos = [17, width/4, (width/4)*2, (width/4)*3, (width/4)*4]

	def new_obstacle(self):
		indice = random.randint(0,4)
		self.liste.append(obstacle(self.bmp2,self.pos[indice]))

	def afficher(self):
		for obstacle in self.liste:
			obstacle.afficher(self.BoxRally)

	def destroy_obs(self):
		for obstacle in self.liste:
			if obstacle.y == self.heigth:
				obstacle.obs_img.SetPosition(wx.Point(1000,1000))
				self.liste.remove(obstacle)

	def collision(self, voiture):
		for obstacle in self.liste:
			if  (((obstacle.y+10< voiture.y+10 and obstacle.y+10 > voiture.y-10) or (obstacle.y-10< voiture.y+10 and obstacle.y-10 > voiture.y-10)) and ((obstacle.x+10 >voiture.x-12 and obstacle.x+10 < voiture.x+12) or (obstacle.x-20 < voiture.x+19 and obstacle.x-20 >voiture.x-19))) :
				return True 

	def descendre(self):
		for obstacle in self.liste:
			obstacle.descendre(2)

	def self_destroy(self):
		for obstacle in self.liste:
			obstacle.obs_img.SetPosition(wx.Point(1000,1000))

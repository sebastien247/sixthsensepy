

import pygame


class voiture:
	def __init__(self, fichier):
		self.image = fichier
		self.x = 200
		self.y = 200

	def gauche (self, pixels):
#		print "gauche"
		self.x = self.x + pixels


	def droite (self, pixels):
#		print "droite"
		self.x = self.x - pixels

	def afficher(self, fenetre):
		affich = pygame.image.load(self.image).convert()
		fenetre.blit(affich, (self.x,self.y))
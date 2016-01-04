import pygame
from pygame.locals import *

from voiture import *
from Constantes import *
from direction import *

class Racing:
	
	pygame.init()

	#Ouverture de la fenetre Pygame (carre : largeur = hauteur)
	fenetre = pygame.display.set_mode((450, 450))
	#Icone
	icone = pygame.image.load(image_icone)
	pygame.display.set_icon(icone)
	#Titre
	pygame.display.set_caption(titre_fenetre)

	#boucle princale

	continuer = 1
	passage = 1
	fond = pygame.image.load(image_fond).convert()
	fenetre.blit(fond, (0,0))
	voiture1 = voiture(image_voiture)

	while continuer:
		fenetre.blit(fond, (0,0))
		voiture1.afficher(fenetre)
		pygame.display.flip()
		
		pygame.time.Clock().tick(30)
		
		for event in pygame.event.get():
			
				#Si l'utilisateur quitte, on met la variable qui continue le jeu
				
				if event.type == QUIT:
					continuer = 0

				elif event.type == KEYDOWN:
					#Si l'utilisateur presse Echap ici, on revient seulement au menu
					if event.key == K_ESCAPE:
						continuer = 0		
				#Touches de deplacement 
					elif event.key == K_RIGHT:
						voiture1.droite(5)
					elif event.key == K_LEFT:
						voiture1.gauche(5)

		manager = Mgr_direction()
		manager.recup_dG()
		manager.recup_dD()
		manager.delta()
		if manager.gauche :
			print "gauche"
		elif manager.droite :
			print "droite"


		pygame.display.flip()
					

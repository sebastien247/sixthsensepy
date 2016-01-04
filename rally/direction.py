

class Mgr_direction:
	def __init__(self):
		self.gauche=False
		self.droite=False
		self.diff=0
		self.dG=0
		self.dD=0

	
	def recup_dG(self, Y):
		self.dG=Y
	
	def recup_dD(self, Y):
		self.dD=Y

	def delta(self):
		self.diff = self.dG - self.dD
		if self.diff < -3:
			self.gauche= True
			self.droite= False
		elif self.diff > 3:
			self.droite = True
			self.gauche= False
		else:
			self.gauche=False
			self.droite=False 
		return self.diff


	def gauche(self):
		return self.gauche

	def droite(self):
		return self.droite

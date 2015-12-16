#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
wxsimulement.py
Permet d'utiliser simulement avec l'interface wxPython.
"""

## Import des modules
#Modules standard
import os
import wx
import locale


## Classe principale (fenêtre)
class MainFrame(wx.Frame):
	
	#Fenêtre d'affichage de simulement.
	
	
	def __init__(self ,parent):
		# Attributs généraux
		loc= locale.getdefaultlocale() # propriétés de l'interface wxPython
		self.int_encode= loc[1] # Encodage de l'interface
		
		# Eléments de la fenêtre principale
		wx.Frame.__init__(self, parent, -1, u'Simulement'.encode\
		(self.int_encode, 'replace'),\
		(0, 0), (-1, -1)) # Initialisation classe parente
		self.Panel= wx.Panel(self, size=(-1, -1))
		
		self.disp= wx.Window(self.Panel, pos=(-1, -1), size=(-1, -1))
		
		
		##############################
		bmp= wx.Bitmap(os.path.realpath('image/nuage-noir-avec-de-la-pluie.jpg'))
		self.img = wx.StaticBitmap(self.disp, -1)
		self.img.SetBitmap(bmp)
		self.img.SetToolTipString("Bonjour Lexileduval !")
		##############################
		
		
		# Organisation du panneau principal
		sizer_glob= wx.BoxSizer(wx.HORIZONTAL)
		sizer_glob.Add(self.disp, 1, wx.EXPAND) # Schéma
		self.Panel.SetSizer(sizer_glob)
		
		self.SetSize((600, 600))
		
		
		## Classe utilitaire complexe : interface générale
class Application(wx.App):
	def OnInit(self):
		"""Ouvre la fenêtre principale"""
		fen = MainFrame(None)
		self.SetTopWindow(fen)
		fen.Show(True)
		return True


## Corps du module :
if __name__ == '__main__': # si ce module est lancé directement :
	app= Application(redirect=True)
	app.MainLoop() 
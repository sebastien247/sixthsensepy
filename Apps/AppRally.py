#coding=utf-8
from App import App
import wx
from pykeyboard import PyKeyboard
import threading
import os
import time
from Apps.rally.voiture import *
from Apps.rally.Constantes import *
from Apps.rally.direction import *
from Apps.rally.voiture import *
from Apps.rally.obstacle import *
from Apps.rally.Mgr_Obstacle import *
import random

class AppRally(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)

        self.name = "rally"
        self.ResetEnvironmentOnStart = False
        self.ResetEnvironmentOnEnd = False
        self._Rally = False
        self.button = wx.Button(self.tabPageApps,label="Rally",pos=(1*self.Grid,13*self.Grid), size=(8*self.Grid,2*self.Grid))

        self.box = wx.StaticBox(self.wuw,pos=(0*self.Grid,16*self.Grid), size=(35*self.Grid,38*self.Grid))
        self.BoxRally = self.box
        self.box.Hide()

        self.after_init()

    def start(self):
        self._Rally = True
        self.Premier = True
        self.status = True

        self.box.Show()
        self.Rally()


    def end(self):
        self.box.Hide()
        self._Rally = False
        self.voiture1.car_img.SetPosition(wx.Point(1000,1000))
        self.text.SetPosition(wx.Point(1000,1000))
        self.manager_obs.self_destroy()

    def Rally(self):
        if self.Premier : 
            #initialisation des differentes images de l'application
            bmp1 = wx.Image(image_voiture, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            bmp2 = wx.Image(image_obstacle, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bmp3 = wx.Image(image_explosion, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

            #creation des objets voitures, manager direction et manager obstacles
            self.voiture1 = voiture(bmp1)
            self.voiture1.afficher(self.BoxRally)
            self.manager = Mgr_direction()
            self.manager_obs = Mgr_Obstacle(bmp2, self.BoxRally, 35*self.Grid, 38*self.Grid)
            self.manager_obs.new_obstacle()
            self.compteur = 0
            self.decompte = 10 



        if self._Rally and self.status:
            self.Premier = False 


            #gestion de la generation des obstacles au bout d'un certains temps
            self.compteur += 1
            if self.compteur ==  self.decompte : 
                self.decompte = random.randint(20,90)
                self.compteur = 0
                self.manager_obs.new_obstacle() 

            #detecteur de collision entre la voiture et un mur
            if self.manager_obs.collision(self.voiture1) :
                #self.voiture1.image = self.bmp3
                self.text = wx.StaticText(self.BoxRally,-1,"Vous avez Perdu",pos=(60,150))
                font = wx.Font(23, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
                self.status = False
                self.text.SetFont(font)


            # Gestion des differents affichages    
            self.manager_obs.afficher()
            self.manager_obs.destroy_obs()
            self.manager_obs.descendre()
            self.manager_obs.collision(self.voiture1)
            self.voiture1.afficher(self.BoxRally)

            if self.wuw.m.CurrData.Present and self.wuw.n.CurrData.Present:
                #mise a jour des coordonées 
                self.manager.recup_dG(self.wuw.m.CurrData.Y)
                self.manager.recup_dD(self.wuw.n.CurrData.Y)

                self.manager.delta()
                if self.manager.gauche:
                    self.voiture1.gauche(3)
                elif self.manager.droite:
                    self.voiture1.droite(3)

            #rappel de la fonction elle meme
            wx.CallLater(10,self.Rally)
#coding=utf-8

from App import App
from AppClock import AppClock
from AppPhoto import AppPhoto
import wx
import os

class AppLearn(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)
        self.name = "Learn"

        self.button = wx.Button(self.tabPageApps, label="Learn", pos=(10*self.Grid,4*self.Grid), size=(8*self.Grid,2*self.Grid))

        self.appClock = AppClock(WuwPanel)
        self.appPhoto = AppPhoto(WuwPanel)

        self.graphics()

        self.after_init()

    def screenTwo(self):
        self.staticBmpCircle.Hide()
        self.screenOne_text.Hide()
        self.screenTwo_text.Show()
        self.staticBmpClose.Show()
        self.appClock.Start()
        self.appClock.actions = {"close": self.screenThree}

    def screenThree(self):
        self.WuwPanel.closeCurrentApp()
        self.actions = {"photo": self.screenFour}
        self.staticBmpClose.Hide()
        self.screenTwo_text.Hide()
        self.staticBmptriangle.Show()
        self.screenThree_text.Show()

    def screenFour(self):
        self.staticBmptriangle.Hide()
        self.screenThree_text.Hide()
        self.screenFour_text.Show()
        self.appPhoto.Start()
        self.appPhoto.actions = {"close": self.screenFive}

    def screenFive(self):
        self.WuwPanel.closeCurrentApp()
        self.actions = {}
        self.staticBmptriangle.Hide()
        self.screenFour_text.Hide()
        self.staticBmpClose.Show()
        self.screenFive_text.Show()

    def start(self):
        self.actions = {"clock":self.screenTwo}
        self.staticBmpCircle.Show()
        self.screenOne_text.Show()

    def end(self):
        self.staticBmpCircle.Hide()
        self.screenOne_text.Hide()
        self.screenTwo_text.Hide()
        self.staticBmptriangle.Hide()
        self.screenThree_text.Hide()
        self.screenFour_text.Hide()
        self.screenFive_text.Hide()
        self.staticBmpClose.Hide()

    def graphics(self):
        # --- Parametres general
        self.learnFont = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        # --- Box d'affichage
        # self.BoxLearn.screenOne=wx.StaticBox(self, pos=(18*self.Grid,16*self.Grid), size=(64*self.Grid,48*self.Grid))
        # self.BoxLearn.SetBackgroundColour("green")

        # --- Premiere ecrans - Demande lancement horloge
        self.path_circle = os.path.realpath('images/circle.png')
        self.img_circle = wx.Image(self.path_circle,wx.BITMAP_TYPE_PNG)
        self.bmp_circle = wx.BitmapFromImage(self.img_circle)
        self.pos_circle = ((self.WuwPanel.Width/2) - self.bmp_circle.Size[0]/2, (self.WuwPanel.Height/2) - self.bmp_circle.Size[1]/2)
        self.staticBmpCircle = wx.StaticBitmap(self.WuwPanel, wx.ID_ANY, self.bmp_circle, pos=self.pos_circle)

        self.screenOneChar = "Bienvenue dans l'apprentissage de SixthSense.\nPour lancer votre première application, reproduisez le cercle \ndevant vous à l'aide de votre doigt."
        self.screenOne_text = wx.StaticText(self.WuwPanel, -1, self.screenOneChar, pos=(self.WuwPanel.Width/2, self.WuwPanel.Height-5), style=wx.ALIGN_CENTRE, size=(self.WuwPanel.Width,self.WuwPanel.Height))
        self.screenOne_text.SetFont(self.learnFont)
        self.sTextOneSizer = self.screenOne_text.GetTextExtent(self.screenOneChar)
        self.screenOne_text.SetPosition(((self.WuwPanel.Width/2)-self.sTextOneSizer[0]/2, self.WuwPanel.Height-5-self.sTextOneSizer[1]))
        self.screenOne_text.SetForegroundColour(wx.Colour(255,255,255))
        
        self.staticBmpCircle.Hide()
        self.screenOne_text.Hide()

        # --- Deuxieme ecrans - Confirmation lancement horloge
        self.path_close = os.path.realpath('images/close.png')
        self.img_close = wx.Image(self.path_close, wx.BITMAP_TYPE_PNG)
        self.bmp_close = wx.BitmapFromImage(self.img_close)
        self.pos_close = ((self.WuwPanel.Width/2) - self.bmp_close.Size[0]/2, (self.WuwPanel.Height/1.4) - self.bmp_close.Size[1]/2)
        self.staticBmpClose = wx.StaticBitmap(self.WuwPanel, wx.ID_ANY, self.bmp_close, pos=self.pos_close)

        self.screenTwoChar = "Félicitations, vous venez de lancer votre première application.\nMaintenant, fermez-la en réalisant le geste de fermeture."
        self.screenTwo_text = wx.StaticText(self.WuwPanel, -1, self.screenTwoChar, pos=(self.WuwPanel.Width/2, self.WuwPanel.Height-5), style=wx.ALIGN_CENTRE, size=(self.WuwPanel.Width,self.WuwPanel.Height))
        self.screenTwo_text.SetFont(self.learnFont)
        self.sTextTwoSizer = self.screenTwo_text.GetTextExtent(self.screenTwoChar)
        self.screenTwo_text.SetPosition(((self.WuwPanel.Width/2)-self.sTextTwoSizer[0]/2, self.WuwPanel.Height-5-self.sTextTwoSizer[1]))
        self.screenTwo_text.SetForegroundColour(wx.Colour(255,255,255))

        self.staticBmpClose.Hide()
        self.screenTwo_text.Hide()

        # --- Troisieme ecrans - Demande lancement photo
        self.path_triangle = os.path.realpath('images/triangle.png')
        self.img_triangle = wx.Image(self.path_triangle,wx.BITMAP_TYPE_PNG)
        self.bmp_triangle = wx.BitmapFromImage(self.img_triangle)
        self.staticBmptriangle = wx.StaticBitmap(self.WuwPanel,wx.ID_ANY,self.bmp_triangle,pos=((self.WuwPanel.Width/2) - self.bmp_triangle.Size[0]/2, (self.WuwPanel.Height/2) - self.bmp_triangle.Size[1]/2))

        self.screenThreeChar = "Cette fois, prenez une photo en reproduissant cette forme."
        self.screenThree_text = wx.StaticText(self.WuwPanel, -1, self.screenThreeChar, pos=(self.WuwPanel.Width/2, self.WuwPanel.Height-5), style=wx.ALIGN_CENTRE, size=(self.WuwPanel.Width,self.WuwPanel.Height))
        self.screenThree_text.SetFont(self.learnFont)
        sTextThreeSizer = self.screenThree_text.GetTextExtent(self.screenThreeChar)
        self.screenThree_text.SetPosition(((self.WuwPanel.Width/2)-sTextThreeSizer[0]/2, self.WuwPanel.Height-5-sTextThreeSizer[1]))
        self.screenThree_text.SetForegroundColour(wx.Colour(255,255,255))
        
        self.staticBmptriangle.Hide()
        self.screenThree_text.Hide()

        # --- Quatrieme ecran - Fermeture de l'app photo
        self.screenFourChar = "Felicitations, vous venez de lancer votre seconde application.\nVous pouvez fermer l'application comme précédemment."
        self.screenFour_text = wx.StaticText(self.WuwPanel, -1, self.screenFourChar, pos=(self.WuwPanel.Width/2, self.WuwPanel.Height-5), style=wx.ALIGN_CENTRE, size=(self.WuwPanel.Width,self.WuwPanel.Height))
        self.screenFour_text.SetFont(self.learnFont)
        self.sTextFourSizer = self.screenFour_text.GetTextExtent(self.screenFourChar)
        self.screenFour_text.SetPosition(((self.WuwPanel.Width/2)-self.sTextFourSizer[0]/2, self.WuwPanel.Height-5-self.sTextFourSizer[1]))
        self.screenFour_text.SetForegroundColour(wx.Colour(255,255,255))
        
        self.screenFour_text.Hide()

        # --- Cinquième ecran - Fermeture de l'application Learn
        self.screenFiveChar = "L'apprentissage est maintenant terminé.\nVous pouvez fermer le tutoriel et commencer à utiliser SixthSense."
        self.screenFive_text = wx.StaticText(self.WuwPanel, -1, self.screenFiveChar, pos=(self.WuwPanel.Width/2, self.WuwPanel.Height-5), style=wx.ALIGN_CENTRE, size=(self.WuwPanel.Width,self.WuwPanel.Height))
        self.screenFive_text.SetFont(self.learnFont)
        self.sTextFiveSizer = self.screenFive_text.GetTextExtent(self.screenFiveChar)
        self.screenFive_text.SetPosition(((self.WuwPanel.Width/2)-self.sTextFiveSizer[0]/2, self.WuwPanel.Height-5-self.sTextFiveSizer[1]))
        self.screenFive_text.SetForegroundColour(wx.Colour(255,255,255))
        
        self.screenFive_text.Hide()
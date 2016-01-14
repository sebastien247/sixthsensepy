from App import App
import wx
import time

class AppClock(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)

        self.timeUpdating = []

        self.name = "clock"
        self.button = wx.Button(self.tabPageApps,label="Clock",pos=(1*self.Grid,1*self.Grid), size=(8*self.Grid,2*self.Grid))
        self.graphics()

        self.clock.Hide()
        
        self.after_init()

    def graphics(self):
        self.fontClock = wx.Font(38, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        # self.box = wx.StaticBox(self.wuw,pos=(40*self.Grid,30*self.Grid), size=(20*self.Grid,20*self.Grid))
        self.charClock = str(time.strftime("%H:%M:%S", time.localtime(time.time())))
        self.clock = wx.StaticText(self.WuwPanel,-1, '', pos=((self.WuwPanel.Width/2,self.WuwPanel.Height/2)))
        self.clock.SetFont(self.fontClock)
        self.sizeClock = self.clock.GetTextExtent(self.charClock)
        self.clock.SetPosition(((self.WuwPanel.Width/2-self.sizeClock[0]/2,self.WuwPanel.Height/2-self.sizeClock[1]/2)))
        self.clock.SetForegroundColour(wx.Colour(255,255,255))

    def updateText(self):
        self.clock.SetLabelText(str(time.strftime("%H:%M:%S", time.localtime(time.time()))))
        if self.launched:
            wx.CallLater(1000, self.updateText)

    def start(self):
        self.updateText()
        self.clock.Show()

    def end(self):
        self.clock.Hide()
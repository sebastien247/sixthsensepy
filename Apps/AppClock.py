from App import App
import wx
import time

class AppClock(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)

        self.timeUpdating = []

        self.name = "clock"
        self.button = wx.Button(self.tabPageApps,label="Clock",pos=(1*self.Grid,1*self.Grid),
                                       size=(8*self.Grid,2*self.Grid))

        self.box = wx.StaticBox(self.wuw,pos=(40*self.Grid,30*self.Grid),
                                   size=(20*self.Grid,20*self.Grid))

        self.box.threadTime=None
        self.box.Hide()
        self.box.Bind(wx.EVT_PAINT, self.show_time)
        
        self.after_init()

    def show_time(self):
        for i in self.timeUpdating:
            i.Destroy()
        self.timeUpdating = []
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.clock = wx.StaticText(self.box,-1, str(time.strftime("%H:%M:%S", time.localtime(time.time()))),pos=(self.Grid*50/10,self.Grid*80/10))
        self.clock.SetFont(font)
        self.clock.SetForegroundColour(wx.Colour(255,255,255))
        timeValue = self.timeUpdating.append(self.clock)
        wx.CallLater(1000, self.show_time)

    def start(self):
        self.box.threadTime = self.wuw.ThreadTime("time", 1, self.box)
        self.box.threadTime.start()
        self.show_time()
        self.box.Show()

    def end(self):
        self.box.threadTime.stop()
        self.box.threadTime=None
        self.box.Hide()
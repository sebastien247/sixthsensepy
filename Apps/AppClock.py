from App import App
import wx

class AppClock(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)

        self.name = "clock"
        self.button = wx.Button(self.tabPageApps,label="Clock",pos=(1*self.Grid,1*self.Grid),
                                       size=(8*self.Grid,2*self.Grid))

        self.box = wx.StaticBox(self.wuw,pos=(40*self.Grid,30*self.Grid),
                                   size=(20*self.Grid,20*self.Grid))

        self.box.threadTime=None
        self.box.Hide()
        self.box.Bind(wx.EVT_PAINT, self.show_time)
        
        self.after_init()

    def show_time(self, event):
        dc = wx.PaintDC(self.box)
        dc.Clear()
        dc.DrawText(time.strftime("%H:%M:%S", time.localtime(time.time())),
                    8*self.Grid,8*self.Grid)

    def start(self):
        self.box.threadTime = self.wuw.ThreadTime("time", 1, self.box)
        self.box.threadTime.start()
        self.box.Show()

    def end(self):
        self.box.threadTime.stop()
        self.box.threadTime=None
        self.box.Hide()
from App import App
import wx
import TouchlessLib

class AppPhoto(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)

        self.name = "photo"
        self.button = wx.Button(self.tabPageApps,label="Photo",pos=(1*self.Grid,4*self.Grid), size=(8*self.Grid,2*self.Grid))

        self.box = wx.StaticBitmap(self.wuw, wx.ID_ANY, pos=(18*self.Grid,16*self.Grid), size=(64*self.Grid,48*self.Grid))

        self.box.Hide()
        self.box.Bind(wx.EVT_PAINT, self.draw_photo)
        
        self.after_init()

    def draw_photo(self):
        if self.wuw.get_latestFrame() == None:
            return
        if self.wuw.get_isDown():
            return
        bmp = TouchlessLib.ImageToBitmap(self.wuw.__latestFrame)
        dc = wx.PaintDC(self.box)
        dc.DrawBitmap(bmp,0,0)

    def start(self):
        self.box.Show()
        img = self.wuw.get_touchlessMgr().CurrentCamera.GetCurrentImage()
        bmp = TouchlessLib.ImageToBitmap(img)
        self.box.SetBitmap(bmp)

    def end(self):
        self.box.Hide()
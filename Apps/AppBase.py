from App import App
import wx

class AppBase(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)
        self.name = "base"

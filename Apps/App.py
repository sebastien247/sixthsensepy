import wx

class App:
    def __init__(self, WuwPanel):
        self.name = ""
        self.button = None
        self.box = None
        self.launched = False
        self.WuwPanel = self.wuw = WuwPanel
        self.link_wuw()
        self.actions = {}

    def after_init(self):
        if self.button:
            self.button.Bind(wx.EVT_BUTTON, self.click_button)

    def click_button(self, event):
        if self.launched:
            self.End()
        else:
            self.Start()

    def link_wuw(self):
        self.tabPageApps = self.wuw.tabPageApps
        self.Grid = self.wuw.Grid
        self.labelDemoName = self.wuw.labelDemoName
        self.ResetEnvironment = self.wuw.ResetEnvironment

    def start(self):
        pass

    def end(self):
        pass

    def Start(self):
        self.launched = True
        self.ResetEnvironment()
        self.labelDemoName.Label = self.name.title()
        self.wuw.apps.append(self)
        if self.button:
            self.button.Label = "Stop " + self.name.title()

        self.start()

    def End(self):
        self.end()
        self.ResetEnvironment()
        self.labelDemoName.Label = "WUW"

        if self.button:
            self.button.Label = self.name.title()

        self.launched = False
        self.wuw.apps.pop()

from App import App
import wx
from pykeyboard import PyKeyboard
import threading
import os
import time

class AppBook(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)

        self.name = "book"
        self.ResetEnvironmentOnStart = False
        self.ResetEnvironmentOnEnd = False

        self.button = wx.Button(self.tabPageApps,label="Book",pos=(10*self.Grid,1*self.Grid),
                                       size=(8*self.Grid,2*self.Grid))

        
        self.actions = {"pdf_left_move":self.leftMove,
                        "pdf_right_move3":self.rightMove
                        }

        self.after_init()

    def leftMove(self):
        k = self.k
        k.press_key(k.control_l_key)
        k.tap_key(k.page_up_key)
        k.release_key(k.control_l_key)

    def rightMove(self):
        k = self.k
        k.press_key(k.control_l_key)
        k.tap_key(k.page_down_key)
        k.release_key(k.control_l_key)

    def start(self):
        self.k = PyKeyboard()
        pdf = self.PdfThread()
        pdf.start()

    def end(self):
        os.system("ps aux | grep -i firefox | awk {'print $2'} | xargs kill -9")


    class PdfThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            os.system("evince tests/test.pdf")

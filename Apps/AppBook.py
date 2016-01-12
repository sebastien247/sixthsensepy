from App import App
import wx
from pykeyboard import PyKeyboard
import threading
import os

class AppBook(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)

        self.name = "book"
        self.button = wx.Button(self.tabPageApps,label="Book",pos=(10*self.Grid,1*self.Grid),
                                       size=(8*self.Grid,2*self.Grid))

        self.after_init()
        self.actions = {"pdf_left_move":self.leftMove,
                        "close":self.end,
                        "pdf_right_move":self.rightMove
                        }


    def book(self):
        """Display the pdf when the middle button of the mouse is pressed"""
        pdf = self.PdfThread()
        pdf.start()
        k = PyKeyboard()
        time.sleep(2)

    def leftMove(self):
        k.press_key(k.control_l_key)
        k.tap_key(k.page_up_key)
        k.release_key(k.control_l_key)

    def rightMove(self):
        k.press_key(k.control_l_key)
        k.tap_key(k.page_down_key)
        k.release_key(k.control_l_key)

    def start(self):
        os.system("evince tests/test.pdf")
        self.book()

    def end(self):
        os.system("ps aux | grep -i firefox | awk {'print $2'} | xargs kill -9")


    class PdfThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            os.system("evince tests/test.pdf")

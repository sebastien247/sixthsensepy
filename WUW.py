#!/usr/bin/python
from gi.repository import Gtk as gtk

class WUW:

    def __init__(self):
        interface = gtk.Builder()
        interface.add_from_file('wuw.glade')

        self.myLabel = interface.get_object("WUW - SixthSense By 3IL")
        interface.connect_signals(self)

        print interface


    def on_mainWindow_destroy(self, widget):
        gtk.main_quit()


if __name__ == "__main__":
    WUW()
    gtk.main()
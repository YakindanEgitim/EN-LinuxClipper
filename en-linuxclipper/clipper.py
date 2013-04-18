from gi.repository import Gtk, Gdk, GdkPixbuf

class Clipper:
    def __init__(self):
        pass

    def capture_screen(self):
        root_win = Gdk.get_default_root_window()

        width, height = root_win.get_width(), root_win.get_height()
        result, x_orig, y_orig = root_win.get_origin()

        screenshot = GdkPixbuf.Pixbuf(root_win, x_orig, y_orig, width, height)
        screenshot.save("/tmp/testshot.png", "png")
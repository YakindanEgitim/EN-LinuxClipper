import cairo
from gi.repository import Gtk, Gdk
from enapi import ENAPI
import subprocess
import StringIO

class Clipper:
    def __init__(self):
        pass

    def capture_screen(self):
        subprocess.call(['/usr/bin/canberra-gtk-play','--id','screen-capture'])
        root_win = Gdk.get_default_root_window()

        width, height = root_win.get_width(), root_win.get_height()
        thumb_surface = Gdk.Window.create_similar_surface(root_win,
                                                          cairo.CONTENT_COLOR,
                                                          width, height)
        cairo_context = cairo.Context(thumb_surface)
        Gdk.cairo_set_source_window(cairo_context, root_win, 0, 0)
        cairo_context.paint()

        dummy_file = StringIO.StringIO()
        thumb_surface.write_to_png(dummy_file)
        ENAPI.upload_image(dummy_file.getvalue())

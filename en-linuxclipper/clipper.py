from gi.repository import Gdk

import cairo
import subprocess
import StringIO
import datetime

from enapi import ENAPI
from config import ConfigManager
from i18n import _


class Clipper:
    """ 
    This class contains Gtk parts of application like capturing 
    screen or window.
    """
    def __init__(self):
        pass

    def capture_screen(self):
        """ 
        Find root window, get capture with cairo and create new note with that
        attachment. Attachment's mime is 'image/png' and note title is 
        Screenshot {date}
        
        === TO DO: Add some error handling code ===
        """

        self.play_capture_sound()
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

        now = datetime.datetime.now()
        ENAPI.create_note(
            title=_("Screenshot ") + now.strftime("%Y-%m-%d %H:%M"),
            attachment_data=dummy_file.getvalue(),
            attachment_mime='image/png'
            )

    def capture_window(self):
        """
        Find active window, get capture with cairo and create new note with that
        attachment. Attachment's mime is 'image/png' and note title is
        Screenshot {date}

        === TO DO: Add some error handling code ===
        """

        self.play_capture_sound()
        screen = Gdk.Screen.get_default()
        active_win = screen.get_active_window()

        width, height = active_win.get_width(), active_win.get_height()
        thumb_surface = Gdk.Window.create_similar_surface(active_win,
                                                          cairo.CONTENT_COLOR,
                                                          width, height)
        cairo_context = cairo.Context(thumb_surface)
        Gdk.cairo_set_source_window(cairo_context, active_win, 0, 0)
        cairo_context.paint()

        dummy_file = StringIO.StringIO()
        thumb_surface.write_to_png(dummy_file)

        now = datetime.datetime.now()
        ENAPI.create_note(
            title=_("Screenshot ") + now.strftime("%Y-%m-%d %H:%M"),
            attachment_data=dummy_file.getvalue(),
            attachment_mime='image/png'
            )

    def capture_selection(self):
        """ Not implemented yet. """

        pass

    def play_capture_sound(self):
        """ Play sound effect when screen or window captured. """
        
        if not ConfigManager.get_conf('play-sound'):
            return

        subprocess.call(['/usr/bin/canberra-gtk-play', 
            '--id', 'screen-capture'])

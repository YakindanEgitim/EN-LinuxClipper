# -*- coding: utf-8; -*-
"""
Copyright (C) 2013 - Özcan ESEN <ozcanesen@gmail.com>

This file is part of EN-LinuxClipper.

EN-LinuxClipper is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

EN-LinuxClipper is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

from gi.repository import Gdk, Gtk, GLib

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
        ENAPI.create_note(title=_("Screenshot ") + now.strftime("%Y-%m-%d %H:%M"),
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
        ENAPI.create_note(title=_("Screenshot ") + now.strftime("%Y-%m-%d %H:%M"),
                          attachment_data=dummy_file.getvalue(),
                          attachment_mime='image/png'
                          )

    def capture_selection(self):
        """ Create new SelectionWindow instance """

        SelectionWindow()

    def play_capture_sound(self):
        """ Play sound effect when screen or window captured. """

        if not ConfigManager.get_conf('play-sound'):
            return

        try:
            subprocess.call(['/usr/bin/canberra-gtk-play',
                            '--id', 'screen-capture'])
        except:
            print "[ERROR] Can't find canberra-gtk-play executable"

class SelectionWindow(Gtk.Window):
    def __init__(self):
        """ Init Selection Window  """
        super(SelectionWindow, self).__init__()

        # basic window properties
        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_keep_above(True)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))

        # configure masks and connect events

        event_mask = (Gdk.EventMask.BUTTON_PRESS_MASK   |
                      Gdk.EventMask.BUTTON_RELEASE_MASK |
                      Gdk.EventMask.EXPOSURE_MASK       |
                      Gdk.EventMask.KEY_PRESS_MASK      |
                      Gdk.EventMask.KEY_RELEASE_MASK    |
                      Gdk.EventMask.ENTER_NOTIFY_MASK   |
                      Gdk.EventMask.LEAVE_NOTIFY_MASK   |
                      Gdk.EventMask.POINTER_MOTION_MASK |
                      Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        self.add_events(event_mask)

        self.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_button_press)
        self.connect("button-release-event", self.on_button_release)
        self.connect("motion-notify-event", self.on_motion_notify)
        self.connect('key-press-event', self.on_keypress)
        
        # init true rgba transparency
        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual != None and self.screen.is_composited():
            self.set_visual(self.visual)

        # get screenshot
        root_win = Gdk.get_default_root_window()
        width, height = root_win.get_width(), root_win.get_height()
        self.screenshot = Gdk.Window.create_similar_surface(root_win,
                                                          cairo.CONTENT_COLOR,
                                                          width, height)
        cairo_context = cairo.Context(self.screenshot)
        Gdk.cairo_set_source_window(cairo_context, root_win, 0, 0)
        cairo_context.paint()

        # this is for rectangle border animation
        self.offset = 0
        self.increase_offset()

        # show window and init default rectangle
        self.fullscreen()
        #self.show_all()
        self.present()
        self.clear_rectangle()

        # change cursor
        cursor = Gdk.Cursor.new(Gdk.CursorType.CROSSHAIR)
        self.get_window().set_cursor(cursor)

    def increase_offset(self):
        self.offset += 1
        GLib.timeout_add(40, self.increase_offset)
        self.queue_draw()

    def clear_rectangle(self):
        """ Set default rectangle """
        self.drawing = False
        self.finished = False
        self.mousex1 = 0
        self.mousey1 = 0
        self.mousex2 = 0
        self.mousey2 = 0
        self.queue_draw()

    def on_motion_notify(self, widget, event):
        """ Started draw and moving mouse. """
        if self.drawing:
            self.mousex2 = event.x
            self.mousey2 = event.y

            # call on_draw function to update window.
            self.queue_draw()

    def on_button_press(self, widget, event):
        """ Start drawing """
        self.drawing = True
        self.mousex1 = event.x
        self.mousey1 = event.y

    def on_button_release(self, widget, event):
        """ Finish drawing """
        self.finished = True
        self.drawing = False
        self.mousex2 = event.x
        self.mousey2 = event.y

    def on_draw(self, widget, cr):
        """ This function drawing rectangle and other things. """

        # fill window with semi-transparent screenshot
        cr.set_source_surface(self.screenshot, 0, 0)
        cr.paint_with_alpha(0.6)

        # if we have a rectangle to draw.
        if self.drawing or self.finished:
            # draw normal screenshot into rectangle area
            cr.set_source_surface(self.screenshot, 0, 0)
            cr.rectangle(self.mousex1,self.mousey1,self.mousex2 - self.mousex1,self.mousey2 - self.mousey1)
            cr.fill()

            # draw border for rectangle.
            cr.set_source_rgba(1, 0, 0, 0.5)
            cr.set_dash([5,5,10,5], self.offset)
            cr.set_line_width(1.5)
            cr.rectangle(self.mousex1,self.mousey1,self.mousex2 - self.mousex1,self.mousey2 - self.mousey1)
            cr.stroke()

    def on_keypress(self, widget, event):
        """ This function looks for key events. """

        # get key name
        keyval = Gdk.keyval_name(event.keyval).lower()

        if keyval == 'escape':
            # close window
            self.hide()
            self.destroy()

        elif keyval == 'delete':
            # delete current rectangle and set it to default
            self.clear_rectangle()

        elif keyval == 'return' and self.finished:
            # hide selection window immediately
            self.hide()
            while Gtk.events_pending():
                Gtk.main_iteration()

            # play sound
            Clipper().play_capture_sound()

            # create new image surface 
            # mousex2 - mousex1 = width
            # mousey2 - mousey1 = height
            # abs: because people can start drawing right to left
            # int: because mouse coordinates are float.
            clip = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(abs(self.mousex2 - self.mousex1)), int(abs(self.mousey2 - self.mousey1)))
            clip_context = cairo.Context(clip)

            # min: (look abs).
            clip_context.set_source_surface(self.screenshot, 0 - min(int(self.mousex1), int(self.mousex2)), 0 - min(int(self.mousey1), int(self.mousey2)))
            clip_context.paint()

            # write to stream and upload
            dummy_file = StringIO.StringIO()
            clip.write_to_png(dummy_file)

            now = datetime.datetime.now()
            ENAPI.create_note(title=_("Clip ") + now.strftime("%Y-%m-%d %H:%M"),
                              attachment_data=dummy_file.getvalue(),
                              attachment_mime='image/png'
                              )

            self.destroy()

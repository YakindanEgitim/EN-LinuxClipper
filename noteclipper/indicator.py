# -*- coding: utf-8; -*-
"""
Copyright (C) 2013 - Özcan ESEN <ozcanesen@gmail.com>

This file is part of NoteClipper.

NoteClipper is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

NoteClipper is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

from gi.repository import Gtk, Gdk
try:
    from gi.repository import AppIndicator3 as appindicator
    use_status_icon = False
except ImportError:
    use_status_icon = True

import mimetypes
import datetime

from i18n import _
from clipper import Clipper
from auth import AuthWin
from enapi import ENAPI
from common import HOST
from preferences import Preferences


class Indicator:
    """ This class holding indicator object and popup menu. """
    def __init__(self):
        """ Define indicator object """

        self.icon_name = "noteclipper"

        if use_status_icon:
            self.ind = Gtk.StatusIcon()
            self.ind.set_from_icon_name(self.icon_name)
            self.ind.set_visible(True)
            self.ind.connect('popup-menu', self.status_icon_callback)
        else:
            self.ind = appindicator.Indicator.new("notify", self.icon_name,
                                                  appindicator.IndicatorCategory.APPLICATION_STATUS)
            self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        # connect update menu function and ENAPI class.
        # so enapi class can update popup menu when connected or disconected.
        ENAPI.update_popup_menu_callback = self.update_popup_menu
        self.update_popup_menu()

    def status_icon_callback(self, icon, button, time):
        """
        Status icon different than indicator, needs callback to show a popup menu.
        """
        self.menu.popup(None, None, lambda menu, icon: Gtk.StatusIcon.position_menu(menu, icon), icon, button, time)
        

    def update_popup_menu(self):
        """
        Update popup menu items by login status, This function will be used by
        ENAPI class.
        """
        menu = Gtk.Menu()

        if ENAPI.is_logged():
            #Show username if logged
            username = Gtk.MenuItem(_("Logged as ") + ENAPI.get_username())
            username.connect('activate', self.open_evernote_homepage)
            menu.append(username)
        else:
            #Show Authorize link if not logged
            auth_user = Gtk.MenuItem(_("Authorize"))
            auth_user.connect('activate', self.auth_user_callback)
            menu.append(auth_user)

        menu.append(Gtk.SeparatorMenuItem.new())

        capture_screen = Gtk.MenuItem(_("Capture Full Screen"))
        capture_screen.connect('activate', self.capture_screen_callback)
        menu.append(capture_screen)

        capture_window = Gtk.MenuItem(_("Capture Window"))
        capture_window.connect('activate', self.capture_window_callback)
        menu.append(capture_window)

        capture_selection = Gtk.MenuItem(_("Capture Selection"))
        capture_selection.connect('activate', self.capture_selection_callback)
        menu.append(capture_selection)

        create_from_file = Gtk.MenuItem(_("Create from file"))
        create_from_file.connect('activate', self.create_from_file_callback)
        menu.append(create_from_file)

        create_from_clipboard = Gtk.MenuItem(_("Create from clipboard"))
        create_from_clipboard.connect('activate',
                                      self.create_from_clipboard_callback)
        menu.append(create_from_clipboard)

        # make capture links unclickable if not logged
        if not ENAPI.is_logged():
            capture_screen.set_sensitive(False)
            capture_window.set_sensitive(False)
            capture_selection.set_sensitive(False)
            create_from_file.set_sensitive(False)
            create_from_clipboard.set_sensitive(False)

        menu.append(Gtk.SeparatorMenuItem.new())

        preferences = Gtk.MenuItem(_("Preferences"))
        preferences.connect('activate', self.open_preferences)
        menu.append(preferences)

        quit = Gtk.MenuItem(_("Quit"))
        quit.connect('activate', self.quit_callback)
        menu.append(quit)

        menu.show_all()

        if use_status_icon:
            self.menu = menu
        else:
            self.ind.set_menu(menu)

    def open_evernote_homepage(self, event):
        """ Open default web browser and navigate Evernote """
        Gtk.show_uri(None, 'https://%s' % HOST, 0)


    def open_preferences(self, event):
        """ Open preferences window """
        Preferences()

    def auth_user_callback(self, event):
        """ Show authentication window. """
        AuthWin()

    def quit_callback(self, event):
        """ Quit application """
        Gtk.main_quit()

    def capture_screen_callback(self, event):
        """
        This is just proxy function that redirects capture request to Clipper
        class
        """
        Clipper().capture_screen()

    def capture_window_callback(self, event):
        """
        Works as capture screen.
        """
        Clipper().capture_window()

    def capture_selection_callback(self, event):
        """
        Works as capture screen.
        """
        Clipper().capture_selection()


    def create_from_clipboard_callback(self, event):
        """
        Get image data from X clipboard if available, and create new note with
        that image.
        """
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        image = clipboard.wait_for_image()

        if image != None:
            image_data = image.save_to_bufferv('png', [], [])[1]

            now = datetime.datetime.now()
            ENAPI.create_note(
                title=_("Clipboard ") + now.strftime("%Y-%m-%d %H:%M"),
                attachment_data=image_data,
                attachment_mime='image/png')

        text = clipboard.wait_for_text()
        if text != None:
            now = datetime.datetime.now()
            ENAPI.create_note(
                title=_("Clipboard ") + now.strftime("%Y-%m-%d %H:%M"),
                note_content=text)

    def create_from_file_callback(self, event):
        """
        Open new Gtk FileChooser dialog, and defined mime type of selected file.
        Create new note with selected file.
        """
        chooser_dialog = Gtk.FileChooserDialog(title=_("Open image"),
                                               action=Gtk.FileChooserAction.OPEN,
                                               buttons=[_("Open"), Gtk.ResponseType.OK, _("Cancel"),
                                               Gtk.ResponseType.CANCEL]
                                               )

        response = chooser_dialog.run()
        filename = chooser_dialog.get_filename()
        chooser_dialog.destroy()

        # we must run gtk main iteration otherwise
        # file chooser dialog will stay on the screen until
        # upload process is done.
        while Gtk.events_pending():
            Gtk.main_iteration()

        if response == Gtk.ResponseType.OK:
            mimetypes.init()
            file_mime = mimetypes.guess_type(filename)[0]
            file_data = open(filename, "rb").read()
            file_title = filename.split("/")[-1]

            ENAPI.create_note(title=file_title,
                              attachment_data=file_data,
                              attachment_mime=file_mime
                              )

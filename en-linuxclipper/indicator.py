from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

import mimetypes

from i18n import _
from clipper import Clipper
from auth import AuthWin
from enapi import ENAPI

class Indicator:
    def __init__(self):
        self.ind = appindicator.Indicator.new("notify", "everpad-mono", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        # this line connects update menu function and ENAPI class
        # so enapi class can update when connected or disconected.
        ENAPI.update_popup_menu_callback = self.update_popup_menu
        self.update_popup_menu()

    def update_popup_menu(self):
        menu = Gtk.Menu()

        if ENAPI.is_logged():
            #Show username if logged
            username = Gtk.MenuItem(_("Logged as ") + ENAPI.get_username())
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
        menu.append(capture_selection)

        create_from_file = Gtk.MenuItem(_("Create from file"))
        create_from_file.connect('activate', self.create_from_file_callback)
        menu.append(create_from_file)

        # make capture links unclickable if not logged
        if not ENAPI.is_logged():
            capture_screen.set_sensitive(False)
            capture_window.set_sensitive(False)
            capture_selection.set_sensitive(False)
            create_from_file.set_sensitive(False)

        menu.append(Gtk.SeparatorMenuItem.new())

        preferences = Gtk.MenuItem(_("Preferences"))
        menu.append(preferences)

        quit = Gtk.MenuItem(_("Quit"))
        quit.connect('activate', self.quit_callback)
        menu.append(quit)

        menu.show_all()
        self.ind.set_menu(menu)

    def auth_user_callback(self, event):
        AuthWin()

    def quit_callback(self, event):
        Gtk.main_quit()

    def capture_screen_callback(self, event):
        Clipper().capture_screen()
        
    def capture_window_callback(self, event):
        Clipper().capture_window()

    def create_from_file_callback(self, event):
        chooser_dialog = Gtk.FileChooserDialog(title=_("Open image"),
            action=Gtk.FileChooserAction.OPEN,
            buttons=[_("Open"), Gtk.ResponseType.OK, _("Cancel"), Gtk.ResponseType.CANCEL]
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

            ENAPI.upload_image(file_data, title=file_title, mime=file_mime)



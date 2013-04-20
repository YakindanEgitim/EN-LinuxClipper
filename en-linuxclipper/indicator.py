from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

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

        # make capture links unclickable if not logged
        if not ENAPI.is_logged():
            capture_screen.set_sensitive(False)
            capture_window.set_sensitive(False)
            capture_selection.set_sensitive(False)

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
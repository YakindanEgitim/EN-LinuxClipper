from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

from i18n import _
from clipper import Clipper

class Indicator:
    def __init__(self):
        self.ind = appindicator.Indicator.new("notify", "everpad-mono", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        menu = Gtk.Menu()

        open_dashboard = Gtk.MenuItem(_("Open Dashboard"))
        menu.append(open_dashboard)
        
        menu.append(Gtk.SeparatorMenuItem.new())

        capture_screen = Gtk.MenuItem(_("Capture Full Screen"))
        capture_screen.connect('activate', self.capture_screen_callback)
        menu.append(capture_screen)

        capture_window = Gtk.MenuItem(_("Capture Window"))
        menu.append(capture_window)

        capture_selection = Gtk.MenuItem(_("Capture Selection"))
        menu.append(capture_selection)

        menu.append(Gtk.SeparatorMenuItem.new())

        preferences = Gtk.MenuItem(_("Preferences"))
        menu.append(preferences)

        quit = Gtk.MenuItem(_("Quit"))
        quit.connect('activate', self.quit_callback)
        menu.append(quit)

        menu.show_all()
        self.ind.set_menu(menu)


    def quit_callback(self, event):
        Gtk.main_quit()

    def capture_screen_callback(self, event):
        Clipper().capture_screen()
        
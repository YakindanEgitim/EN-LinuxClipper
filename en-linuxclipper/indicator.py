
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

class Indicator:
    def __init__(self):
        ind = appindicator.Indicator.new("notify", "everpad-mono", appindicator.IndicatorCategory.APPLICATION_STATUS)
        ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        menu = Gtk.Menu()
        ind.set_menu(menu)

        Gtk.main()

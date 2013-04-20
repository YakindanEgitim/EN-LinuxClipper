from gi.repository import Gtk
from indicator import Indicator
from enapi import ENAPI

ENAPI.connect()
indicator = Indicator()

Gtk.main()

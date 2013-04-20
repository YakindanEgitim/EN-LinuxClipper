from gi.repository import Gtk
from indicator import Indicator
from enapi import ENAPI

indicator = Indicator()
ENAPI.connect()

Gtk.main()

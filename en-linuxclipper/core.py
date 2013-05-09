#!/usr/bin/env python

from gi.repository import Gtk

from indicator import Indicator
from enapi import ENAPI


def main():
    """ Define initial objects and start main loop """

    # Indicator must be defined first, because enapi will call
    # update popup menu callback which was defined in Indicator.
    indicator = Indicator()
    ENAPI.connect()

    Gtk.main()

if __name__ == "__main__":
    main()

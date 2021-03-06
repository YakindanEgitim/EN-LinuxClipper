#!/usr/bin/env python
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

#!/usr/bin/python
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

import glob
import sys
import os

try:
    import DistUtilsExtra.auto
    from DistUtilsExtra.command import *
except ImportError:
    sys.exit(1)

def update_config(values = {}):
    oldvalues = {}
    try:
        fin = file('noteclipper/common.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find noteclipper/common.py")
        sys.exit(1)
    return oldvalues

class install_extra(DistUtilsExtra.auto.install_auto):
    def run(self):
        values = {'DIR_PREFIX': "'%s'" % (self.prefix)}
        previous_values = update_config(values)
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)

DistUtilsExtra.auto.setup(name="noteclipper",
          version="0.1.0",
          description="NoteClipper",
          author="Ozcan ESEN",
          author_email="ozcanesen@gmail.com",
          long_description="Clipping application",
          keywords='evernote clipper note noteclipper',
          url='https://github.com/YakindanEgitim/EN-LinuxClipper',
          license='GPLv3',
          scripts=["bin/noteclipper"],
          packages = ['evernote',
                      'noteclipper',
                      'thrift',
                      'evernote.edam',
                      'evernote.api',
                      'thrift.transport',
                      'thrift.server',
                      'thrift.protocol',
                      'evernote.edam.limits',
                      'evernote.edam.notestore',
                      'evernote.edam.userstore',
                      'evernote.edam.type',
                      'evernote.edam.error'],
          data_files=[('share/icons/hicolor/scalable/apps/', glob.glob("data/icons/*svg")),
                      ('share/noteclipper/', glob.glob("data/share/noteclipper/*")),
                      ('share/applications/', glob.glob("data/share/applications/*desktop"))],
          cmdclass = {"install": install_extra,
                      "build" : build_extra.build_extra,
                      "build_i18n" :  build_i18n.build_i18n,
                      "build_help" : build_help.build_help,
                      "build_icons" : build_icons.build_icons}
          )

#!/usr/bin/python
# -*- coding: utf-8; -*-
"""
Copyright (C) 2013 - Özcan ESEN <ozcanesen@gmail.com>

This file is part of EN-LinuxClipper.

EN-LinuxClipper is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

EN-LinuxClipper is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

from distutils.core import setup
from DistUtilsExtra.command import *

import re
import glob
from subprocess import Popen, PIPE

setup(name="enlinuxclipper",
      version="0.1.0",
      description="Evernote client for Linux desktops",
      author="Ozcan ESEN",
      author_email="ozcanesen@gmail.com",
      long_description="Evernote client for Linux desktops",
      keywords='evernote clipper screenshot enlinuxclipper',
      url='https://github.com/YakindanEgitim/EN-LinuxClipper',
      license='GPLv3',
      scripts=["bin/en-linuxclipper"],
      packages = ['evernote',
                  'enlinuxclipper',
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
                  ('share/applications/', glob.glob("data/desktop/*desktop"))],
      cmdclass = { "build" : build_extra.build_extra,
                   "build_i18n" :  build_i18n.build_i18n,
                   "build_help" : build_help.build_help,
                   "build_icons" : build_icons.build_icons}
      )


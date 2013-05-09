#!/usr/bin/python

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
      packages = ['enlinuxclipper'],
      data_files=[('share/icons/hicolor/scalable/apps/', glob.glob("data/icons/*svg"))],
      cmdclass = { "build" : build_extra.build_extra,
                   "build_i18n" :  build_i18n.build_i18n,
                   "build_help" : build_help.build_help,
                   "build_icons" : build_icons.build_icons}
      )


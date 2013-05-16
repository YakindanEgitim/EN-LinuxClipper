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

from base64 import b64encode, b64decode
import ConfigParser
import os


class ConfigManager():
    """
    This class reponsible for keeping and saving configuration variables
    """

    # set default values
    config = ConfigParser.SafeConfigParser({'access_token': '',
                                           'play-sound': 'True',
                                           'copy-to-clipboard': 'True',
                                           'googl-shortlink': 'True'})

    # config path
    cfg_dir = os.environ['HOME'] + '/.config/en-linuxclipper/'
    cfg_file = 'main.cfg'
    cfg_full_path = cfg_dir + cfg_file

    namespace = 'DEFAULT'
    config.read(cfg_full_path)

    @staticmethod
    def get_conf(key):
        """ Return configuration value for key """
        try:
            value = ConfigManager.config.get(ConfigManager.namespace, key)
        except ConfigParser.Error:
            print ("[DEBUG] No option '%s' found in namespace '%s'." %
                   (key, ConfigManager.namespace))
            return None

        # config parser storing all values as string
        # we need to convert them to python types
        try:
            return int(value)
        except ValueError:
            if value == 'True':
                return True
            elif value == 'False':
                return False
            else:
                if key == 'access_token':
                    # base64 required for parsing file properly
                    # because access_token have many special charachters.
                    value = b64decode(value)
                return value

    @staticmethod
    def set_conf(key, value):
        """ Keep new value for key """
        if key == 'access_token':
            value = b64encode(value)
        try:
            ConfigManager.config.set(ConfigManager.namespace, key, str(value))
        except ConfigParser.Error:
            print ("[DEBUG] No option '%s' found in namespace '%s'." %
                   (key, ConfigManager.namespace))
            return

    @staticmethod
    def save_config():
        """ Save configuration variables to file. """
        if not os.path.exists(ConfigManager.cfg_dir):
            os.mkdir(ConfigManager.cfg_dir)

        with open(ConfigManager.cfg_full_path, 'wb') as configfile:
            ConfigManager.config.write(configfile)


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

from gi.repository import Gtk

from config import ConfigManager
from common import DIR_PREFIX
from i18n import _
from enapi import ENAPI
from auth import AuthWin

import os


class Preferences():

    def __init__(self):
        self.init_ui()

    def init_ui(self):
        builder = Gtk.Builder()
        builder.set_translation_domain('en-linuxclipper')
        builder.add_from_file(DIR_PREFIX + '/share/en-linuxclipper/preferences.ui')

        self.window = builder.get_object('window')
        self.window.set_title(_("Preferences"))

        # control buttons
        self.btn_cancel = builder.get_object('btn_cancel')
        self.btn_cancel.connect('clicked', self.on_cancel_clicked)

        self.btn_ok = builder.get_object('btn_ok')
        self.btn_ok.connect('clicked', self.on_ok_clicked)

        # auth / remove auth button
        self.btn_auth = builder.get_object('btn_auth')
        self.btn_auth.connect('clicked', self.on_auth_clicked)

        if ENAPI.is_logged():
            self.btn_auth.set_label(_('Remove authorization'))
        else:
            self.btn_auth.set_label(_('Authorize'))

        # default notebook combobox
        self.notebooklist = builder.get_object('notebooklist')
        self.notebooklist.set_sensitive(ENAPI.is_logged())

        self.notebooklist.append_text(_("Always use remote default"))
        self.notebooklist.set_active(0)
        item_id = 0

        self._notebooklist = ENAPI.get_notebook_list()
        guid = ConfigManager.get_conf('notebookguid')

        for notebook in self._notebooklist:
            # insert notebook name
            self.notebooklist.append_text(notebook[0])
            item_id = item_id + 1

            # set active if selected
            if guid == notebook[1]:
                self.notebooklist.set_active(item_id)

        # run on startup
        self.chk_startup = builder.get_object('chk_startup')
        self.chk_startup.set_active(os.path.exists(os.environ['HOME'] + '/.config/autostart/EN-LinuxClipper.desktop'))

        # other checkboxes
        self.chk_play_sound = builder.get_object('chk_play_sound')
        self.chk_play_sound.set_active(ConfigManager.get_conf('play-sound'))

        self.chk_share_note = builder.get_object('chk_share_note')
        self.chk_share_note.set_active(ConfigManager.get_conf('copy-to-clipboard'))

        self.chk_googl_shortlinks = builder.get_object('chk_googl_shortlinks')
        self.chk_googl_shortlinks.set_active(ConfigManager.get_conf('googl-shortlink'))

        self.window.show_all()

    def on_ok_clicked(self, widget):
        # save config to file
        ConfigManager.set_conf('play-sound', self.chk_play_sound.get_active())

        ConfigManager.set_conf('copy-to-clipboard', self.chk_share_note.get_active())

        ConfigManager.set_conf('googl-shortlink', self.chk_play_sound.get_active())

        # save default notebook
        if self.notebooklist.get_active() > 0:
            ConfigManager.set_conf('notebookguid', self._notebooklist[self.notebooklist.get_active() - 1][1])
        else:
            ConfigManager.set_conf('notebookguid', '')

        # startup
        desktop_file = DIR_PREFIX + '/share/applications/EN-LinuxClipper.desktop'
        desktop_file_autostart = os.environ['HOME'] + '/.config/autostart/EN-LinuxClipper.desktop'

        if (self.chk_startup.get_active() and not os.path.exists(desktop_file_autostart)):
            os.system('cp ' + desktop_file + ' ' + desktop_file_autostart)

        if (not self.chk_startup.get_active() and os.path.exists(desktop_file_autostart)):
            os.system('rm -f ' + desktop_file_autostart)

        ConfigManager.save_config()

    def on_cancel_clicked(self, widget):
        self.window.hide()

    def on_auth_clicked(self, widget):
        if ENAPI.is_logged():
            ENAPI.disconnect()
            ConfigManager.set_conf('access_token', '')
            ConfigManager.save_config()
        else:
            AuthWin()

        self.window.hide()

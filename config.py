#!/usr/bin/env python

from qt.core import QLabel, QLineEdit, QWidget, QGridLayout
from calibre.utils.config import JSONConfig

# Define the unique configuration key for the plugin
prefs = JSONConfig("plugins/create_mp3")
prefs.defaults = {"run_tts_command": ""}


class ConfigWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.l = QGridLayout()
        self.setLayout(self.l)

        self.l.addWidget(QLabel("Command Path (w/ :BOOK: var):", self), 0, 0)
        self.command_str_edit = QLineEdit(self)
        self.command_str_edit.setText(prefs["run_tts_command"])
        self.l.addWidget(self.command_str_edit, 0, 1)

    def save_settings(self):
        prefs["run_tts_command"] = self.command_str_edit.text().strip()

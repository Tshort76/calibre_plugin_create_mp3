#!/usr/bin/env python

import shlex
from qt.core import QDialog, QMessageBox, QPushButton, QGridLayout
from calibre.gui2 import error_dialog
from calibre_plugins.create_mp3.config import prefs

from calibre_plugins.create_mp3.job import run_external_script

BOOK_PLACEHOLDER = ":BOOK:"


class CreateMP3Dialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config

        self.db = gui.current_db

        self.l = QGridLayout()
        self.setLayout(self.l)

        self.setWindowTitle("Create MP3 Plugin")
        self.setWindowIcon(icon)

        self.check_prefs_button = QPushButton("Create MP3s", self)
        self.check_prefs_button.clicked.connect(self.create_mp3s)
        self.l.addWidget(self.check_prefs_button, 0, 0, 1, 2)

        self.conf_button = QPushButton("⚙️", self)
        self.conf_button.clicked.connect(self.config)
        self.l.addWidget(self.conf_button, 1, 0)

        self.about_button = QPushButton("❔", self)
        self.about_button.clicked.connect(self.about)
        self.l.addWidget(self.about_button, 1, 1)

        self.resize(self.sizeHint())

    def about(self):
        text = get_resources("about.txt")
        QMessageBox.about(self, "About the Create MP3 Plugin", text.decode("utf-8"))

    def _execute_tts(self, book_paths: list[str]):
        _command_str = prefs.get("run_tts_command", None)
        if not (_command_str and BOOK_PLACEHOLDER in _command_str):
            error_dialog(
                self,
                "No TTS command",
                "Please specify the command to run for invoking your TTS engine. Use :BOOK: to indicate when the file_path should be substituted",
                show=True,
            )
            return

        _command = shlex.split(_command_str)
        _idx = _command.index(BOOK_PLACEHOLDER)

        commands = []
        for path in book_paths:
            _command[_idx] = path
            commands.append(_command)

        run_external_script(self.gui, commands)

    def create_mp3s(self):
        book_ids = self.gui.library_view.get_selected_ids()

        if not book_ids:
            error_dialog(self, "No selection", "Please select at least one book.", show=True)
            return

        paths = []
        for book_id in book_ids:
            for fmt in ["txt", "epub", "pdf"]:
                if file_path := self.db.format_abspath(book_id, fmt, index_is_id=True):
                    paths.append(file_path)
                    break

        self._execute_tts(paths)

    def config(self):
        self.do_user_config(parent=self)

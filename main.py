#!/usr/bin/env python

import shlex
from qt.core import QDialog, QMessageBox, QPushButton, QGridLayout
from calibre.gui2 import error_dialog
from calibre_plugins.create_mp3.config import prefs

from calibre_plugins.create_mp3.job import run_external_script

BOOK_PLACEHOLDER = ":BOOK:"


def _dict_to_str(d: dict) -> str:
    "Special format needed for passing in shell command"
    return '"' + str(d).replace("'", "'") + '"'


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

        self.check_prefs_button = QPushButton("Create MP3(s)", self)
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

    def _execute_tts(self, paths_meta: list[tuple[str, str]]):
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
        book_idx = _command.index(BOOK_PLACEHOLDER)
        meta_idx = None
        try:
            meta_idx = _command.index(":META:")
        except ValueError:
            pass

        commands = []
        for path, meta in paths_meta:
            _command[book_idx] = path
            if meta_idx is not None:
                _command[meta_idx] = meta
            commands.append(_command)

        run_external_script(self.gui, commands)

    def create_mp3s(self):
        book_ids = self.gui.library_view.get_selected_ids()

        if not book_ids:
            error_dialog(self, "No selection", "Please select at least one book.", show=True)
            return

        paths = []
        for book_id in book_ids:
            m = self.db.get_metadata(book_id, index_is_id=True)
            cover_path = self.db.cover(book_id, index_is_id=True, as_path=True)
            _meta = {"title": m.title, "author": m.authors[0], "image_path": cover_path}
            meta_str = _dict_to_str(_meta)
            for fmt in ["txt", "epub", "pdf"]:
                if file_path := self.db.format_abspath(book_id, fmt, index_is_id=True):
                    paths.append((file_path, meta_str))
                    break

        self._execute_tts(paths)

    def config(self):
        self.do_user_config(parent=self)

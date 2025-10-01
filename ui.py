#!/usr/bin/env python

from calibre.gui2.actions import InterfaceAction
from calibre_plugins.create_mp3.main import CreateMP3Dialog


class CreateMP3Plugin(InterfaceAction):

    name = "Create MP3 File"

    action_spec = ("Create MP3 File", None, "Run the Create MP3 File", "Ctrl+Shift+F1")

    def genesis(self):
        icon = get_icons("create_mp3.png", "Create MP3")

        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)

    def show_dialog(self):
        base_plugin_object = self.interface_action_base_plugin
        do_user_config = base_plugin_object.do_user_config

        d = CreateMP3Dialog(self.gui, self.qaction.icon(), do_user_config)
        d.show()

    def apply_settings(self):
        from calibre_plugins.create_mp3.config import prefs

        prefs

#!/usr/bin/env python

from calibre.customize import InterfaceActionBase


class CreateMP3PluginWrap(InterfaceActionBase):
    name = "Create MP3"
    description = "A plugin for generating audio files"
    supported_platforms = ["windows", "osx", "linux"]
    author = "Thomas Long"
    version = (1, 0, 0)
    minimum_calibre_version = (8, 0, 0)

    actual_plugin = "calibre_plugins.create_mp3.ui:CreateMP3Plugin"

    def is_customizable(self):
        return True

    def config_widget(self):
        from calibre_plugins.create_mp3.config import ConfigWidget

        return ConfigWidget()

    def save_settings(self, config_widget):
        config_widget.save_settings()

        ac = self.actual_plugin_
        if ac is not None:
            ac.apply_settings()

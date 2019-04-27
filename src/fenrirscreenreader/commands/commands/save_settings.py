#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core import settingsManager

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return 'Saves your current Fenrir settings so they are the default.'
    def run(self):
        self.env['runtime']['settingsManager'].saveSettings(settingConfigPath)
        self.env['runtime']['outputManager'].presentText("Settings saved.", interrupt=True)True
    def setCallback(self, callback):
        pass

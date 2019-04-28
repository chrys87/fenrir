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
        return _('Saves your current Fenrir settings so they are the default.')
    def run(self):
        settingsFile = self.env['runtime']['settingsManager'].getSettingsFile()
        self.env['runtime']['settingsManager'].saveSettings(settingsFile)
        self.env['runtime']['outputManager'].presentText(_("Settings saved."), interrupt=True)
    def setCallback(self, callback):
        pass

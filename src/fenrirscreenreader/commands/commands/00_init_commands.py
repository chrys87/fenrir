#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

# this command is just to initialize stuff.
# like init index lists in memoryManager
# it is not useful to execute it
class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        # clipboard
        self.env['runtime']['memoryManager'].addIndexList('clipboardHistory', self.env['runtime']['settingsManager'].getSettingAsInt('general', 'numberOfClipboards'))
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No description found'         
    def run(self):
        pass
    def setCallback(self, callback):
        pass

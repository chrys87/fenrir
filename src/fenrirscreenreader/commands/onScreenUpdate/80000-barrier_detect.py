#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'      

    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('barrier','enabled'):
            return
        if not self.env['runtime']['screenManager'].isDelta(ignoreSpace=True):
            return      

        self.env['runtime']['barrierManager'].handleLineBarrier(self.env['screen']['newContentText'].split('\n'), self.env['screen']['newCursor']['x'],self.env['screen']['newCursor']['y'])

    def setCallback(self, callback):
        pass


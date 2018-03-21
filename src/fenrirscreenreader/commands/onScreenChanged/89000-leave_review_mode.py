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
        if not self.env['runtime']['settingsManager'].getSettingAsBool('review', 'leaveReviewOnScreenChange'):
            return
        self.env['runtime']['cursorManager'].clearReviewCursor()

    def setCallback(self, callback):
        pass


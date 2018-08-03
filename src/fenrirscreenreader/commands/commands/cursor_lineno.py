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
        return _('Line number for cursor')         
    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        self.env['runtime']['outputManager'].presentText(str(cursorPos['y'] + 1), interrupt=True)
        self.env['runtime']['outputManager'].announceActiveCursor()
        self.env['runtime']['outputManager'].presentText(' line number' , interrupt=False)
        
    def setCallback(self, callback):
        pass

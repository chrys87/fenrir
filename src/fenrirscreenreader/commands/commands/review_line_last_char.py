#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import char_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('Move Review to the last character on the line')

    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        self.env['runtime']['cursorManager'].setReviewCursorPosition(self.env['screen']['columns']-1 ,cursorPos['y'])
        self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], lastChar = \
          char_utils.getLastCharInLine(self.env['screen']['newCursorReview']['y'], self.env['screen']['newContentText'])
        
        self.env['runtime']['outputManager'].presentText(lastChar ,interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False)        
        self.env['runtime']['outputManager'].presentText(_("last character in line"), interrupt=False)
   
    def setCallback(self, callback):
        pass

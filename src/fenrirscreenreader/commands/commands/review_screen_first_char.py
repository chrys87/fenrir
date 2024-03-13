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
        return _('Move Review to the first character on the screen (left top)')

    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        self.env['runtime']['cursorManager'].setReviewCursorPosition(0 ,0)
        self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], lastChar = \
          char_utils.getLastCharInLine(self.env['screen']['newCursorReview']['y'], self.env['screen']['newContentText'])
        
        self.env['runtime']['outputManager'].presentText(lastChar ,interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False)
        self.env['runtime']['outputManager'].presentText(_("first character in screen"), interrupt=False)
   
    def setCallback(self, callback):
        pass

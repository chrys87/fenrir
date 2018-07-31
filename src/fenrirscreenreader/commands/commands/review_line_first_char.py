#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import line_utils
from fenrirscreenreader.utils import char_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('Move Review to the first character on the line')

    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        x, y, currLine = \
          line_utils.getCurrentLine(cursorPos['x'], cursorPos['y'], self.env['screen']['newContentText'])
        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText(_("line is empty"), interrupt=True)
            return          
        self.env['runtime']['cursorManager'].setReviewCursorPosition((len(currLine) - len(currLine.lstrip())), cursorPos['y'])
        self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], currChar = \
          char_utils.getCurrentChar(self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], self.env['screen']['newContentText'])       

        self.env['runtime']['outputManager'].presentText(currChar ,interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False)        
        self.env['runtime']['outputManager'].presentText(_("first character in line indent {0}").format(str(len(currLine) - len(currLine.lstrip()))), interrupt=False)
   
    def setCallback(self, callback):
        pass

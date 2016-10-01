#!/bin/python
from utils import char_utils
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'presents the current character.'        
    
    def run(self):
        self.env['runtime']['cursorManager'].enterReviewModeCurrTextCursor()

        self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], currChar = \
          char_utils.getCurrentChar(self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], self.env['screenData']['newContentText'])
        
        if currChar.strip(" \t\n") == '':
            self.env['runtime']['outputManager'].presentText("blank" ,interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(currChar ,interrupt=True, ignorePunctuation=True, announceCapital=True)
  
    def setCallback(self, callback):
        pass

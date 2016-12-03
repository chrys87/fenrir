#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import char_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'phonetically presents the previous character and set review to it'    
    
    def run(self):
        self.env['runtime']['cursorManager'].enterReviewModeCurrTextCursor()

        self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], prevChar, endOfScreen, lineBreak = \
          char_utils.getPrevChar(self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], self.env['screenData']['newContentText'])
        
        if prevChar.isspace():
            self.env['runtime']['outputManager'].presentText("blank" ,interrupt=True)
        else:
            prevChar = char_utils.getPhonetic(prevChar)
            self.env['runtime']['outputManager'].presentText(prevChar ,interrupt=True, announceCapital=True)
  
    def setCallback(self, callback):
        pass

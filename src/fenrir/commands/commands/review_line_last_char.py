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
        return 'set review cursor to end of current line and display the content'        

    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        self.env['runtime']['cursorManager'].setReviewCursorPosition(self.env['screenData']['columns']-1 ,cursorPos['y'])
        self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], lastChar = \
          char_utils.getLastCharInLine(self.env['screenData']['newCursorReview']['y'], self.env['screenData']['newContentText'])
        
        self.env['runtime']['outputManager'].presentText(lastChar ,interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False)        
        self.env['runtime']['outputManager'].presentText("last char in line", interrupt=False)
   
    def setCallback(self, callback):
        pass

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
        self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], upChar, endOfScreen = \
          char_utils.getUpChar(self.env['screenData']['newCursorReview']['x'],self.env['screenData']['newCursorReview']['y'], self.env['screenData']['newContentText'])
        if upChar.isspace():
            self.env['runtime']['outputManager'].presentText("line is empty" ,interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(upChar ,interrupt=True, ignorePunctuation=True, announceCapital=True)        
   
    def setCallback(self, callback):
        pass

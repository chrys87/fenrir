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
        return 'phonetically presents the current character'    
    
    def run(self):
        if self.env['screenData']['newCursorReview']:
            cursorPos = self.env['screenData']['newCursorReview'].copy()
        else:
            cursorPos = self.env['screenData']['newCursor'].copy()

        x, y, currChar = \
          char_utils.getCurrentChar(cursorPos['x'], cursorPos['y'], self.env['screenData']['newContentText'])
        
        if currChar.strip(" \t\n") == '':
            self.env['runtime']['outputManager'].presentText("blank" ,interrupt=True)
        else:
            currChar = char_utils.getPhonetic(currChar)
            self.env['runtime']['outputManager'].presentText(currChar ,interrupt=True)
  
    def setCallback(self, callback):
        pass

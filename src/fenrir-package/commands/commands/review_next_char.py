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
        return 'moves review to the next character and presents it'        
    
    def run(self):
        self.env['screenData']['oldCursorReview'] = self.env['screenData']['newCursorReview']
        if not self.env['screenData']['newCursorReview']:
            self.env['screenData']['newCursorReview'] = self.env['screenData']['newCursor'].copy()

        self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], currChar = \
          char_utils.getNextChar(self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], self.env['screenData']['newContentText'])
        
        if currChar.strip(" \t\n") == '':
            self.env['runtime']['outputManager'].presentText("blank", interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(currChar, interrupt=True)
   
    def setCallback(self, callback):
        pass

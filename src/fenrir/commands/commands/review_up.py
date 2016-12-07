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
        return 'set review cursor to the char in the line below and present it'        

    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], upChar, endOfScreen = \
          char_utils.getUpChar(self.env['screenData']['newCursorReview']['x'],self.env['screenData']['newCursorReview']['y'], self.env['screenData']['newContentText'])
        self.env['runtime']['outputManager'].presentText(upChar ,interrupt=True, ignorePunctuation=True, announceCapital=True)        
        if endOfScreen:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'endOfScreen'):        
                self.env['runtime']['outputManager'].presentText('end of screen' ,interrupt=False, soundIcon='EndOfScreen')                 
        if lineBreak:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'lineBreak'):        
                self.env['runtime']['outputManager'].presentText('line break' ,interrupt=False, soundIcon='EndOfLine')    
    def setCallback(self, callback):
        pass

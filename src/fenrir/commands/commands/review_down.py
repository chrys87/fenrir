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
        return 'set review cursor to char below the current char and present it.'        

    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], downChar, endOfScreen = \
          char_utils.getDownChar(self.env['screenData']['newCursorReview']['x'],self.env['screenData']['newCursorReview']['y'], self.env['screenData']['newContentText'])
        self.env['runtime']['outputManager'].presentText(downChar ,interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False)
        if endOfScreen:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'endOfScreen'):        
                self.env['runtime']['outputManager'].presentText('end of screen' ,interrupt=True, soundIcon='EndOfScreen')                     
    def setCallback(self, callback):
        pass

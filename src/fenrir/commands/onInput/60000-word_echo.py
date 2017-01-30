#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import word_utils
import string

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'     

    def run(self):
        # first place could not be the end of a word
        if self.env['screenData']['newCursor']['x'] == 0:
            return
        # is it enabled?    
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'wordEcho'):
            return

        # just when cursor move worddetection is needed
        if not self.env['runtime']['cursorManager'].isCursorHorizontalMove():
            return
        if self.env['runtime']['inputManager'].noKeyPressed():
            return  
        # for now no new line
        if self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return
        # get the word            
        newContent = self.env['screenData']['newContentText'].split('\n')[self.env['screenData']['newCursor']['y']]
        x, y, currWord, endOfScreen, lineBreak = \
          word_utils.getCurrentWord(self.env['screenData']['newCursor']['x'], 0, newContent)                          
        # currently writing
        if self.env['runtime']['screenManager'].isDelta():
            return
        else:
        # at the end of a word
            if not newContent[self.env['screenData']['newCursor']['x']].isspace():
                return
            if (x + len(currWord) != self.env['screenData']['newCursor']['x']) and \
              (x + len(currWord) != self.env['screenData']['newCursor']['x']-1):
                return    

        if currWord != '':
            self.env['runtime']['outputManager'].presentText(currWord, interrupt=True, flush=False)

    def setCallback(self, callback):
        pass


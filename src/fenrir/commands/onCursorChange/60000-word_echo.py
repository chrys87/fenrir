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
        # is it enabled?    
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'wordEcho'):
            return

        # just when cursor move worddetection is needed
        if not self.env['runtime']['cursorManager'].isCursorHorizontalMove():
            return
        # for now no new line
        if self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return
        # currently writing
        if self.env['runtime']['screenManager'].isDelta():
            return            
        
        # get the word            
        newContent = self.env['screen']['newContentText'].split('\n')[self.env['screen']['newCursor']['y']]
        x, y, currWord, endOfScreen, lineBreak = \
          word_utils.getCurrentWord(self.env['screen']['newCursor']['x'], 0, newContent)                          
        
        # is there a word?        
        if currWord == '':
            return

        # navigate prev word
        if self.env['screen']['oldCursor']['x'] - self.env['screen']['newCursor']['x'] > 1:
            # at the start of a word        
            if newContent[self.env['screen']['newCursor']['x']].isspace():
                return         
            if self.env['screen']['newCursor']['x'] != x:
                return       
        # navigate next word
        else:
            # at the end of a word        
            if not newContent[self.env['screen']['newCursor']['x']].isspace():
                return
            if (x + len(currWord) != self.env['screen']['newCursor']['x']) and \
              (x + len(currWord) != self.env['screen']['newCursor']['x']-1):
                return    

        self.env['runtime']['outputManager'].presentText(currWord, interrupt=True, flush=False)

    def setCallback(self, callback):
        pass


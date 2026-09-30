#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import word_utils
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

        # is navigation?    
        if not abs(self.env['screen']['oldCursor']['x'] - self.env['screen']['newCursor']['x']) > 1:
            return

        # just when cursor move worddetection is needed
        if not self.env['runtime']['cursorManager'].isCursorHorizontalMove():
            return
        # for now no new line
        if self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return
        # currently writing
        if 'screenManager' in self.env['runtime'] and hasattr(self.env['runtime']['screenManager'], 'isDelta'):
            if self.env['runtime']['screenManager'].isDelta():
                return            
        
        lines = self.env['screen']['newContentText'].split('\n')
        cursorY = self.env['screen']['newCursor']['y']
        if cursorY >= len(lines):
            return
        newContent = lines[cursorY]
        cursorX = self.env['screen']['newCursor']['x']

        # get the word            
        x, y, currWord, endOfScreen, lineBreak = \
          word_utils.getCurrentWord(cursorX, 0, newContent, string.whitespace)                          
        
        # is there a word?        
        if currWord == '':
            return

        # at the start or end of a word        
        if (x + len(currWord) != cursorX) and \
          (cursorX != x):
            return     

        cleanWord = currWord.strip(string.whitespace)
        if cleanWord == '':
            return

        self.env['runtime']['outputManager'].presentText(cleanWord, interrupt=True, flush=False)

    def setCallback(self, callback):
        pass


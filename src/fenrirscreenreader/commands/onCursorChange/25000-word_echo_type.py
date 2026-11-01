#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import word_utils
import string

class command():
    def __init__(self):
        self.lastEchoedWord = None

    def initialize(self, environment):
        self.env = environment
        self.lastEchoedWord = None

    def shutdown(self):
        self.lastEchoedWord = None

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

        delimiters = string.whitespace + string.punctuation

        if 'screenManager' in self.env['runtime'] and hasattr(self.env['runtime']['screenManager'], 'isDelta'):
            if self.env['runtime']['screenManager'].isDelta():
                return            
        
        lines = self.env['screen']['newContentText'].split('\n')
        cursorY = self.env['screen']['newCursor']['y']
        if cursorY >= len(lines):
            return
        newContent = lines[cursorY]
        cursorX = self.env['screen']['newCursor']['x']
        oldX = self.env['screen']['oldCursor']['x']

        # if cursor is on a word character, reset tracking and return
        if cursorX < len(newContent) and newContent[cursorX] not in delimiters:
            self.lastEchoedWord = None
            return

        # only word echo on single-character forward movement
        if cursorX - oldX != 1:
            return

        # get the word            
        x, y, currWord, endOfScreen, lineBreak = \
          word_utils.getCurrentWord(cursorX, 0, newContent, delimiters)                          
        
        # is there a word?        
        if currWord == '':
            return

        # at the end of a word (boundary check)
        if (x + len(currWord) != cursorX) and \
          (x + len(currWord) != cursorX - 1):
            return    

        # do not trigger repeatedly on subsequent delimiter / consecutive whitespace characters
        wordKey = (x, cursorY, currWord)
        if self.lastEchoedWord == wordKey:
            return

        cleanWord = currWord.strip(string.whitespace).rstrip(string.punctuation)
        if cleanWord == '':
            return

        self.lastEchoedWord = wordKey
        self.env['runtime']['outputManager'].presentText(cleanWord, interrupt=True, flush=False)

    def setCallback(self, callback):
        pass

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
        # is naviation?
        if self.env['screen']['newCursor']['x'] - self.env['screen']['oldCursor']['x'] != 1:
            return
        # just when cursor move worddetection is needed
        if not self.env['runtime']['cursorManager'].isCursorHorizontalMove():
            return
        # for now no new line
        if self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return
        delimiters = string.whitespace + string.punctuation
        # currently writing
        lines = self.env['screen']['newContentText'].split('\n')
        if self.env['screen']['newCursor']['y'] >= len(lines):
            return
        newContent = lines[self.env['screen']['newCursor']['y']]
        prevX = self.env['screen']['oldCursor']['x']
        if prevX < 0 or prevX >= len(newContent) or newContent[prevX] not in delimiters:
            return

        # get the word            
        x, y, currWord, endOfScreen, lineBreak = \
          word_utils.getCurrentWord(self.env['screen']['newCursor']['x'], 0, newContent, delimiters)                          
        
        # is there a word?        
        if currWord == '':
            return
        # at the end of a word        
        cursorX = self.env['screen']['newCursor']['x']
        if cursorX < len(newContent) and newContent[cursorX] not in delimiters:
            return
        # at the end of a word        
        if (x + len(currWord) != self.env['screen']['newCursor']['x']) and \
          (x + len(currWord) != self.env['screen']['newCursor']['x']-1):
            return    

        cleanWord = currWord.strip(string.whitespace).rstrip(string.punctuation)
        if cleanWord == '':
            return

        self.env['runtime']['outputManager'].presentText(cleanWord, interrupt=True, flush=False)

    def setCallback(self, callback):
        pass


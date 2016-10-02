#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import word_utils
from utils import char_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'phonetically spells the current word'        
    
    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        x, y, currWord = \
          word_utils.getCurrentWord(cursorPos['x'], cursorPos['y'], self.env['screenData']['newContentText'])
        
        if currWord.isspace():
            self.env['runtime']['outputManager'].presentText("blank", interrupt=True)
        else:
            firstSequence = True
            for c in currWord:
                currChar = char_utils.getPhonetic(c) 
                self.env['runtime']['outputManager'].presentText(currChar, interrupt=firstSequence)
                firstSequence = False
   
    def setCallback(self, callback):
        pass

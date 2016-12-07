#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import word_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'moves review to the next word and presents it'        
    
    def run(self):
        self.env['screenData']['oldCursorReview'] = self.env['screenData']['newCursorReview']
        if self.env['screenData']['newCursorReview'] == None:
            self.env['screenData']['newCursorReview'] = self.env['screenData']['newCursor'].copy()

        self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], nextWord, endOfScreen, lineBreak = \
          word_utils.getNextWord(self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], self.env['screenData']['newContentText'])
        
        if nextWord.isspace():
            self.env['runtime']['outputManager'].presentText("blank", interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(nextWord, interrupt=True)
        if endOfScreen:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'endOfScreen'):        
                self.env['runtime']['outputManager'].presentText('end of screen' ,interrupt=False, soundIcon='EndOfScreen')                 
        if lineBreak:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'lineBreak'):        
                self.env['runtime']['outputManager'].presentText('line break' ,interrupt=False, soundIcon='EndOfLine')    
    def setCallback(self, callback):
        pass

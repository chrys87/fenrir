#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import word_utils
initialized = False
try:
    import enchant
    initialized = True
except:
    pass
    
class command():
    def __init__(self):
        self.language = ''
        self.spellChecker = None
    def initialize(self, environment):
        self.env = environment
        self.updateSpellLanguage()
    def shutdown(self):
        pass
    def getDescription(self):
        return 'removes the current word from the exceptions dictionary'        
    def updateSpellLanguage(self):  
        self.spellChecker = enchant.Dict(self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage'))
        self.language = self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage')      
       
    def run(self):
        if not initialized:
           self.env['runtime']['outputManager'].presentText('pychant is not installed', interrupt=True) 
           return
        if self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage') != self.language:
            try:
                self.updateSpellLanguage()
            except:
                return    

        if self.env['screenData']['newCursorReview']:
            cursorPos = self.env['screenData']['newCursorReview'].copy()
        else:
            cursorPos = self.env['screenData']['newCursor'].copy()
            
        # get the word
        newContent = self.env['screenData']['newContentText'].split('\n')[cursorPos['y']]
        x, y, currWord =  word_utils.getCurrentWord(cursorPos['x'], 0, newContent)                  

        if currWord != '':
            if self.spellChecker.is_removed(currWord):
                self.env['runtime']['outputManager'].presentText(currWord + ' is already removed from dict',soundIcon='Cancel', interrupt=True)                
            else:
                self.spellChecker.remove(currWord)             
                self.env['runtime']['outputManager'].presentText(currWord + ' removed',soundIcon='Accept', interrupt=True)                    

    def setCallback(self, callback):
        pass

#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import word_utils
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
        return _('checks the spelling of the current word')        
    def updateSpellLanguage(self):  
        if not initialized:  
           return            
        self.spellChecker = enchant.Dict(self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage'))
        self.language = self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage')      
       
    def run(self):
        if not initialized:
           self.env['runtime']['outputManager'].presentText(_('pyenchant is not installed'), interrupt=True) 
           return
        if self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage') != self.language:
            try:
                self.updateSpellLanguage()
            except:
                return    
        
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
            
        # get the word
        newContent = self.env['screen']['newContentText'].split('\n')[cursorPos['y']]
        x, y, currWord, endOfScreen, lineBreak = word_utils.getCurrentWord(cursorPos['x'], 0, newContent)                  

        if not currWord.isspace():
            if not self.spellChecker.check(currWord):
                self.env['runtime']['outputManager'].presentText(_('misspelled'),soundIcon='mispell', interrupt=True)
            elif not ignore:
                self.env['runtime']['outputManager'].presentText(_('correct'),soundIcon='', interrupt=True)            
    def setCallback(self, callback):
        pass

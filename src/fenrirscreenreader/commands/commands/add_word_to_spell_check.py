#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import word_utils
import string
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
        return _('adds the current word to the exceptions dictionary')        
    def updateSpellLanguage(self):  
        self.spellChecker = enchant.Dict(self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage'))
        self.language = self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage')      
    
    def run(self):
        if not initialized:
           self.env['runtime']['outputManager'].presentText(_('pyenchant is not installed'), interrupt=True) 
           return
        if self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage') != self.language:
            try:
                self.updateSpellLanguage()
            except Exception as e:
                return    
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        # get the word
        newContent = self.env['screen']['newContentText'].split('\n')[cursorPos['y']]
        x, y, currWord, endOfScreen, lineBreak =  word_utils.getCurrentWord(cursorPos['x'], 0, newContent)
        currWord = currWord.strip(string.whitespace + '!"#$%&\()*+,-./:;<=§>?@[\\]^_{|}~')

        if currWord != '':
            if self.spellChecker.is_added(currWord):
                self.env['runtime']['outputManager'].presentText(_('{0} is already in dictionary').format(currWord,), soundIcon='Cancel', interrupt=True)                
            else:
                self.spellChecker.add(currWord)             
                self.env['runtime']['outputManager'].presentText(_('{0} added to dictionary').format(currWord,), soundIcon='Accept', interrupt=True)               

    def setCallback(self, callback):
        pass

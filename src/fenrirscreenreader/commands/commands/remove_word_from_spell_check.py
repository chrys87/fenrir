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
        return _('removes the current word from the exceptions dictionary')        
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
            except:
                return    

        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
            
        # get the word
        newContent = self.env['screen']['newContentText'].split('\n')[cursorPos['y']]
        x, y, currWord, endOfScreen, lineBreak =  word_utils.getCurrentWord(cursorPos['x'], 0, newContent)                  
        currWord = currWord.strip(string.whitespace + '!"#$%&\()*+,-./:;<=§>?@[\\]^_{|}~')
        if not currWord.isspace():
            if self.spellChecker.is_removed(currWord):
                self.env['runtime']['outputManager'].presentText(_('{0} is not in the dictionary').format(currWord,), soundIcon='Cancel', interrupt=True)                
            else:
                self.spellChecker.remove(currWord)             
                self.env['runtime']['outputManager'].presentText(_('{0} removed').format(currWord,), soundIcon='Accept', interrupt=True)                    
    def setCallback(self, callback):
        pass

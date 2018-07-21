#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import word_utils
import os, string

initialized = False
try:
    import enchant
    initialized = True
except:
    pass
    
class command():
    def __init__(self):
        self.language = ''
        self.spellChecker = ''
    def initialize(self, environment):
        self.env = environment
        self.updateSpellLanguage()
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'
      
    def updateSpellLanguage(self):  
        if not initialized:
           self.env['runtime']['outputManager'].presentText('pychant is not installed', interrupt=True) 
           return
        self.spellChecker = enchant.Dict(self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage'))
        self.language = self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage')      

    def run(self):
        if not initialized:
            return        
        if not self.env['runtime']['settingsManager'].getSettingAsBool('general', 'autoSpellCheck'):
            return
        if self.env['runtime']['settingsManager'].getSetting('general', 'spellCheckLanguage') != self.language:
            try:
                self.updateSpellLanguage()
            except:
                return

        # just when horizontal cursor move worddetection is needed
        if not self.env['runtime']['cursorManager'].isCursorHorizontalMove():
            return
            
        # for now no new line
        if self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return
        # more than a keyecho?
        if len(self.env['screen']['newDelta']) > 1:
            return            
        # deletion
        if self.env['runtime']['screenManager'].isNegativeDelta():
            return             
        # first place could not be the end of a word
        if self.env['screen']['newCursor']['x'] == 0:
            return
            
        # get the word (just for speedup only look at current line
        newContent = self.env['screen']['newContentText'].split('\n')[self.env['screen']['newCursor']['y']]
        x, y, currWord, endOfScreen, lineBreak = word_utils.getCurrentWord(self.env['screen']['newCursor']['x'], 0, newContent)                  
        # was this a typed word?
        if self.env['runtime']['screenManager'].isDelta():
            if not(newContent[self.env['screen']['oldCursor']['x']] in string.whitespace + '!"#$%&()*+,-./:;<=>?@[\\]^_{|}~' and x != self.env['screen']['oldCursor']['x']):
                return
            else:
                currWord = currWord.strip(string.whitespace + '!"#$%&()*+,-./:;<=>?@[\\]^_{|}~')
        else:
        # or just arrow arround?
            if not newContent[self.env['screen']['newCursor']['x']].isspace():
                return
            if (x + len(currWord) != self.env['screen']['newCursor']['x']) and \
              (x + len(currWord) != self.env['screen']['newCursor']['x']-1):
                return  

        # just on end of word
        if self.env['screen']['newCursor']['x'] > 0:
            if not newContent[self.env['screen']['oldCursor']['x'] - 1].lower() in string.ascii_lowercase:
                return
        
        # ignore bash buildins
        if currWord in ['cd','fg','bg','alias','bind','dir','caller','buildin','command','declare','echo','enable','help','let','local','logout',\
          'mapfile','printf','read','readarray','source','type','typeset','ulimit','unalias']:
            return
        # ignore the application name
        if currWord.upper() == 'FENRIR':
            return       
        if currWord[0] =='-':
            return
        if currWord[0] == '/':
            return
        if currWord[0] == '#':
            return
        if currWord.startswith('./'):
            return               
        if '@' in currWord and '.' in currWord:
            return            
        if currWord[0] == '@':
            return            
        if currWord.isnumeric():
            return            
        if currWord.isdecimal():
            return
        if currWord.isspace():
            return
  
        try:
            if os.path.exists("/bin/"+currWord):
                return
        except:
            pass
        try:
            if os.path.exists("/usr/bin/"+currWord):
                return            
        except:
            pass
        try:
            if os.path.exists("/sbin/"+currWord):
                return            
        except:
            pass

        if not self.spellChecker.check(currWord):
            self.env['runtime']['outputManager'].presentText(_('misspelled'), soundIcon='mispell', interrupt=False, flush=False)

    def setCallback(self, callback):
        pass


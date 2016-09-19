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
        self.spellChecker = ''
    def initialize(self, environment):
        self.updateSpellLanguage(environment)
    def shutdown(self, environment):
        pass 
    def getDescription(self, environment):
        return 'No Description found'        
     def updateSpellLanguage(self, environment):  
        self.spellChecker = enchant.Dict(environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage'))
        self.language = environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage')      
      
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'general', 'autoSpellCheck'):
            return

        if not initialized:
           return
        if environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage') != self.language:
            try:
                self.updateSpellLanguage(environment)
            except:
               return

        # just when cursor move worddetection is needed
        if environment['screenData']['newCursor']['x'] == environment['screenData']['oldCursor']['x']:
            return 
            
        # for now no new line
        if environment['screenData']['newCursor']['y'] != environment['screenData']['oldCursor']['y']:
            return 
        if len(environment['screenData']['newDelta']) > 1:
            return            
            
        # TTY Change is no new word
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return
            
        # first place could not be the end of a word
        if environment['screenData']['newCursor']['x'] == 0:
            return
            
        # get the word
        newContent = environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']]
        x, y, currWord =  word_utils.getCurrentWord(environment['screenData']['newCursor']['x'], 0, newContent)                  
        # was this a typed word?
        if environment['screenData']['newDelta'] != '':
            if not(newContent[environment['screenData']['oldCursor']['x']].strip(" \t\n") == '' and x != environment['screenData']['oldCursor']['x']):
                return
        else:
        # or just arrow arround?
            if not(newContent[environment['screenData']['newCursor']['x']].strip(" \t\n") == '' and x != environment['screenData']['newCursor']['x']):
                return            

        if currWord != '':
            if not self.spellChecker.check(currWord):
                environment['runtime']['outputManager'].presentText(environment, 'misspelled',soundIcon='mispell', interrupt=True)

    def setCallback(self, callback):
        pass

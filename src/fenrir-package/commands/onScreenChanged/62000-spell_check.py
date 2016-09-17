#!/bin/python
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
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return 'No Description found'        
    
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'general', 'autoSpellCheck'):
            return environment

        if not initialized:
           return environment
        if environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage') != self.language:
            try:
                self.spellChecker = enchant.Dict(environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage'))
                self.language = environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage')
            except:
               return environment

        # just when cursor move worddetection is needed
        if environment['screenData']['newCursor']['x'] == environment['screenData']['oldCursor']['x']:
            return environment 
            
        # for now no new line
        if environment['screenData']['newCursor']['y'] != environment['screenData']['oldCursor']['y']:
            return environment 
        if len(environment['screenData']['newDelta']) > 1:
            return environment            
            
        # TTY Change is no new word
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return environment
            
        # first place could not be the end of a word
        if environment['screenData']['newCursor']['x'] == 0:
            return environment
            
        # get the word
        newContent = environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']]
        x, y, currWord =  word_utils.getCurrentWord(environment['screenData']['newCursor']['x'], 0, newContent)                  
        # was this a typed word?
        if environment['screenData']['newDelta'] != '':
            if not(newContent[environment['screenData']['oldCursor']['x']].strip() == '' and x != environment['screenData']['oldCursor']['x']):
                return environment
        else:
        # or just arrow arround?
            if not(newContent[environment['screenData']['newCursor']['x']].strip() == '' and x != environment['screenData']['newCursor']['x']):
                return environment            

        if currWord != '':
            if not self.spellChecker.check(currWord):
                environment['runtime']['outputManager'].presentText(environment, 'misspelled',soundIcon='mispell', interrupt=True)

        return environment
    def setCallback(self, callback):
        pass

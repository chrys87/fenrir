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
        self.spellChecker = None
    
    def run(self, environment):
        if not initialized:
           environment['runtime']['outputManager'].presentText(environment, 'pychant is not installed', interrupt=True) 
           return environment
        if environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage') != self.language:
            try:
                self.spellChecker = enchant.Dict(environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage'))
                self.language = environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage')
            except:
                return environment    

        if (environment['screenData']['newCursorReview'] != None):
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()
            
        # get the word
        newContent = environment['screenData']['newContentText'].split('\n')[cursorPos['y']]
        x, y, currWord =  word_utils.getCurrentWord(cursorPos['x'], 0, newContent)                  

        if currWord != '':
            if not self.spellChecker.check(currWord):
                environment['runtime']['outputManager'].presentText(environment, 'misspelled',soundIcon='mispell', interrupt=True)

        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

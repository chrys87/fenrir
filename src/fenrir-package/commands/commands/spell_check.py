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
    
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'general', 'autoSpellCheck'):
            return environment

        if not initialized:
           environment['runtime']['outputManager'].presentText(environment, 'pychant is not installed', interrupt=True) 
           return environment
        if environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage') != self.language:
            try:
                spellChecker = enchant.Dict(environment['runtime']['settingsManager'].getSetting(environment, 'general', 'spellCheckLanguage'))
            except:
                return environment    

        if (environment['screenData']['newCursorReview'] != None):
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()
            
        # get the word
        newContent = environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']]
        x, y, currWord =  word_utils.getCurrentWord(cursorPos['x'], 0, newContent)                  

        if currWord != '':
            if not spellChecker.check(currWord):
                environment['runtime']['outputManager'].presentText(environment, 'misspelled', interrupt=True)

        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

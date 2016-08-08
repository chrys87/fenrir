#!/bin/python
from utils import word_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'wordEcho'):
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
        if not(newContent[environment['screenData']['newCursor']['x']].strip(" \t\n") == '' and x != environment['screenData']['newCursor']['x']):
            return environment
        print('word')
        if currWord != '':
            environment['runtime']['outputManager'].presentText(environment, currWord, interrupt=True)

        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

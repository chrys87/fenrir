#!/bin/python
from utils import word_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass  
    def getDescription(self, environment):
        return ''        

    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'wordEcho'):
            return
   
        # just when cursor move worddetection is needed
        if environment['screenData']['newCursor']['x'] == environment['screenData']['oldCursor']['x']:
            return 
            
        # for now no new line
        if environment['screenData']['newCursor']['y'] != environment['screenData']['oldCursor']['y']:
            return environment 
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
            if not(newContent[environment['screenData']['oldCursor']['x']].strip() == '' and x != environment['screenData']['oldCursor']['x']):
                return
        else:
        # or just arrow arround?
            if not(newContent[environment['screenData']['newCursor']['x']].strip() == '' and x != environment['screenData']['newCursor']['x']):
                return            

        if currWord != '':
            environment['runtime']['outputManager'].presentText(environment, currWord, interrupt=True)

    def setCallback(self, callback):
        pass


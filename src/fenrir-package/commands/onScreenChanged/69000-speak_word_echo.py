#!/bin/python
from utils import word_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'wordEcho'):
            return environment
   
        # just when typing is a new word
        if environment['screenData']['newCursor']['x'] <= environment['screenData']['oldCursor']['x']:
            return environment 

        # TTY Change is no new word
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return environment

        # here we just arrow arround (left right) no changes
        if environment['screenData']['newDelta'] == environment['screenData']['oldDelta'] and \
          environment['screenData']['newNegativeDelta'] == '':
            return environment
        # this is not the end of the word
        if environment['screenData']['newDelta'] == environment['screenData']['oldDelta'] and \
          environment['screenData']['newNegativeDelta'] != ' ':
            return environment

        # japp its a finished word... announce it:x
        newContent = environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']]
        x, y, currWord =  word_utils.getCurrentWord(environment['screenData']['newCursor']['x'], 0, newContent)
        
        if environment['screenData']['newCursor']['x'] > 0 and \
          newContent[environment['screenData']['newCursor']['x']- 1] == ' ':
            environment['runtime']['outputManager'].presentText(environment, currWord, interrupt=True)

        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

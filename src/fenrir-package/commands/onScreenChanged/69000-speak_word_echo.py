#!/bin/python
from utils import word_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        return environment
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'wordEcho') and\
          environment['screenData']['newCursor']['x'] <= environment['screenData']['oldCursor']['x']:
            return environment 

        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return environment

        if environment['screenData']['newDelta'] == environment['screenData']['oldDelta']:
            return environment

        newContent = environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']]
        x, y, currWord =  word_utils.getCurrentWord(environment['screenData']['newCursorReview']['x'], 0, newContent)

        if environment['screenData']['newCursor']['x'] > 0 and \
          newContent[environment['screenData']['newCursor']['x'] - 1] == ' ':
            environment['runtime']['outputManager'].presentText(environment, currWord, interrupt=True)
            print('word')
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

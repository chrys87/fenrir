#!/bin/python
from utils import word_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = environment['screenData']['newCursorReview']
        if (environment['screenData']['newCursorReview']['y'] == -1) or \
          (environment['screenData']['newCursorReview']['x'] == -1):
            environment['screenData']['newCursorReview'] = environment['screenData']['newCursor'].copy()

        environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], currWord = \
          word_utils.getCurrentWord(environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], environment['screenData']['newContentText'])
        
        if currWord.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, currWord, interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

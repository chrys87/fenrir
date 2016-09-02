#!/bin/python
from utils import word_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'No Description found'        
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = environment['screenData']['newCursorReview']
        if environment['screenData']['newCursorReview'] == None:
            environment['screenData']['newCursorReview'] = environment['screenData']['newCursor'].copy()

        environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], currWord = \
          word_utils.getCurrentWord(environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], environment['screenData']['newContentText'])
        
        if currWord.strip() == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, currWord, interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass

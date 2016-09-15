#!/bin/python
from utils import word_utils
from utils import char_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'phonetically spells the current word'        
    def run(self, environment):
        if (environment['screenData']['newCursorReview'] != None):
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()
        x, y, currWord = \
          word_utils.getCurrentWord(cursorPos['x'], cursorPos['y'], environment['screenData']['newContentText'])
        
        if currWord.strip() == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", interrupt=True)
        else:
            firstSequence = True
            for c in currWord:
                currChar = char_utils.getPhonetic(c) 
                environment['runtime']['outputManager'].presentText(environment, currChar, interrupt=firstSequence)
                firstSequence = False
        return environment    
    def setCallback(self, callback):
        pass

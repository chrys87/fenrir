#!/bin/python
from utils import char_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'phonetically presents the current character'    
    def run(self, environment):
        if (environment['screenData']['newCursorReview'] != None):
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()

        x, y, currChar = \
          char_utils.getCurrentChar(cursorPos['x'], cursorPos['y'], environment['screenData']['newContentText'])
        
        if currChar.strip() == '':
            environment['runtime']['outputManager'].presentText(environment, "blank" ,interrupt=True)
        else:
            currChar = char_utils.getPhonetic(currChar)
            environment['runtime']['outputManager'].presentText(environment, currChar ,interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass

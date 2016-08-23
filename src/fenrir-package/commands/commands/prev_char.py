#!/bin/python
from utils import char_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = environment['screenData']['newCursorReview']
        if environment['screenData']['newCursorReview'] == None:
            environment['screenData']['newCursorReview'] = environment['screenData']['newCursor'].copy()

        environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], currChar = \
          char_utils.getPrevChar(environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], environment['screenData']['newContentText'])
        
        if currChar.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, currChar, interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

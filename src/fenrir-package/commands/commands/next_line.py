#!/bin/python
from utils import line_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = environment['screenData']['newCursorReview']
        if (environment['screenData']['newCursorReview']['y'] == -1) or \
          (environment['screenData']['newCursorReview']['x'] == -1):
            environment['screenData']['newCursorReview'] = environment['screenData']['newCursor'].copy()

        environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], currLine = \
          line_utils.getNextLine(environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], environment['screenData']['newContentText'])
        
        if currLine.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank")
        else:
            environment['runtime']['outputManager'].presentText(environment, currLine)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

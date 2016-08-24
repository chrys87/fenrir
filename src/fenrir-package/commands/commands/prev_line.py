#!/bin/python
from utils import line_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = environment['screenData']['newCursorReview']
        if environment['screenData']['newCursorReview'] == None:
            environment['screenData']['newCursorReview'] = environment['screenData']['newCursor'].copy()

        environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], currLine = \
          line_utils.getPrevLine(environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], environment['screenData']['newContentText'])
        
        if currLine.strip() == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", soundIcon='EmptyLine', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, currLine, interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

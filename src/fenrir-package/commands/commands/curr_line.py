#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = environment['screenData']['newCursorReview']
        if environment['screenData']['newCursorReview']['y'] == -1:
            environment['screenData']['newCursorReview'] = environment['screenData']['newCursor'].copy()
        wrappedLines = environment['screenData']['newContentText'].split('\n')          
        if wrappedLines[environment['screenData']['newCursorReview']['y']].strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank")
        else:
            environment['runtime']['outputManager'].presentText(environment, wrappedLines[environment['screenData']['newCursorReview']['y']])
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

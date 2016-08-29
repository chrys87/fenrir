#!/bin/python
from utils import char_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['newCursorReview'] = 'x:0,y:0'

        environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], currChar = \
        
        environment['runtime']['outputManager'].presentText(environment, "Top Left", interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

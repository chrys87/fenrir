#!/bin/python
from utils import char_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['newCursorReview'] = {'x':environment [screenData][columns],'y':0}

        environment['runtime']['outputManager'].presentText(environment, "Bottom", interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

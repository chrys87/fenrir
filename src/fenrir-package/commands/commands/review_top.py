#!/bin/python
from utils import char_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return 'move review to top of screen'        

    def run(self, environment):
        environment['screenData']['newCursorReview'] = {'x':0,'y':0}

        environment['runtime']['outputManager'].presentText(environment, "Top", interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass

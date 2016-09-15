#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):   
        return environment 
    def getDescription(self):
        return 'move review to bottom of screen'         
    def run(self, environment):
        environment['screenData']['newCursorReview'] = { 'x': 0, 'y':environment['screenData']['lines']}
        environment['runtime']['outputManager'].presentText(environment, "Bottom", interrupt=True)     
        return environment
    def setCallback(self, callback):
        pass

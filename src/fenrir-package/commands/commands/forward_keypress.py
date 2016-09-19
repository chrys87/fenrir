#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'sends the following keypress to the terminal'        
    
    def run(self, environment):
        environment['input']['keyForeward'] = True
        environment['runtime']['outputManager'].presentText(environment, 'Foreward next keypress', interrupt=True)

    def setCallback(self, callback):
        pass

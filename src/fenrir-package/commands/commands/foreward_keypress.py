#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'No Description found'        
    def run(self, environment):
        environment['input']['keyForeward'] = True
        environment['runtime']['outputManager'].presentText(environment, 'Foreward next keypress', interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass

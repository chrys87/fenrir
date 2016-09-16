#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'displays the last received text'        
    def run(self, environment):
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass

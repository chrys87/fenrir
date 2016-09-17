#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return 'interrupts the current presentation'        
    
    def run(self, environment):
        environment['runtime']['outputManager'].interruptOutput(environment)
    def setCallback(self, callback):
        pass

#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return 'exits Fenrir'        
    
    def run(self, environment):
        environment['generalInformation']['running'] = False
        return environment    
    def setCallback(self, callback):
        pass


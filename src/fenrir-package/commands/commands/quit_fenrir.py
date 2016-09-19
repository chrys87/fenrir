#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'exits Fenrir'        
    
    def run(self, environment):
        environment['generalInformation']['running'] = False

    def setCallback(self, callback):
        pass


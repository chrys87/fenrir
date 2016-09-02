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
        if environment['screenData']['newContentText'].strip() == '':
            environment['runtime']['outputManager'].presentText(environment, "screen is empty", soundIcon='EmptyLine', interrupt=True)
        else:    
           environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newContentText'],interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass

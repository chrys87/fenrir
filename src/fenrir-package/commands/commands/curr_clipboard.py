#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return 'speaks the contents of the currently selected clipboard'       

    def run(self, environment):
        if len(environment['commandBuffer']['clipboard']) == 0:
            environment['runtime']['outputManager'].presentText(environment, 'clipboard empty', interrupt=True)
            return environment 
        environment['runtime']['outputManager'].presentText(environment, environment['commandBuffer']['clipboard'][environment['commandBuffer']['currClipboard']], interrupt=True)
        return environment                
    def setCallback(self, callback):
        pass

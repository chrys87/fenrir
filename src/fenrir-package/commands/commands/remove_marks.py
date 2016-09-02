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
        environment['commandBuffer']['Marks']['1'] = None
        environment['commandBuffer']['Marks']['2'] = None
        environment['commandBuffer']['Marks']['3'] = None
        environment['runtime']['outputManager'].presentText(environment, 'Remove marks', interrupt=True)
        return environment
    def setCallback(self, callback):
        pass

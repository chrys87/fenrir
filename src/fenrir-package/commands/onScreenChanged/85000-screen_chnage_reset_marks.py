#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return ''        

    def run(self, environment):
        if environment['screenData']['newTTY'] == environment['screenData']['oldTTY']:
            return environment
        environment['commandBuffer']['Marks']['1']  = None
        environment['commandBuffer']['Marks']['2']  = None
        environment['commandBuffer']['Marks']['3']  = None
        return environment
    def setCallback(self, callback):
        pass


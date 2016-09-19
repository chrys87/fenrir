#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass 
    def getDescription(self, environment):
        return ''        

    def run(self, environment):
        if environment['screenData']['newTTY'] == environment['screenData']['oldTTY']:
            return
        environment['commandBuffer']['Marks']['1']  = None
        environment['commandBuffer']['Marks']['2']  = None
        environment['commandBuffer']['Marks']['3']  = None

    def setCallback(self, callback):
        pass


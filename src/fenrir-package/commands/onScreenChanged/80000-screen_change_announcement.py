#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return ''        
    def run(self, environment):
        if environment['screenData']['newTTY'] == environment['screenData']['oldTTY']:
            return environment
        environment['runtime']['outputManager'].presentText(environment, "screen " + str(environment['screenData']['newTTY']),soundIcon='ChangeTTY', interrupt=True)         
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=False)

        return environment
    def setCallback(self, callback):
        pass


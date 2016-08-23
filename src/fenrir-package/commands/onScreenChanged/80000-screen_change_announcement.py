#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):

        if environment['screenData']['newTTY'] == environment['screenData']['oldTTY']:
            return environment
        environment['runtime']['outputManager'].playSoundIcon(environment,'ChangeTTY')            
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=True)

        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

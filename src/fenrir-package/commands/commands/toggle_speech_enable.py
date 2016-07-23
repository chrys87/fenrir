#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['speech']['enabled'] = not environment['speech']['enabled']
        if environment['speech']['enabled']: 
            environment['runtime']['outputManager'].presentText(environment, "speech enabled")
        else:
            environment['runtime']['outputManager'].presentText(environment, "speech disabled")
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

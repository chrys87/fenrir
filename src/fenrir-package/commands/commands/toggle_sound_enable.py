#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['sound']['enabled'] = not environment['sound']['enabled']
        if environment['sound']['enabled']: 
            environment['runtime']['outputManager'].presentText(environment, "sound enabled")
        else:
            environment['runtime']['outputManager'].presentText(environment, "sound disabled")
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

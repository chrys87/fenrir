#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['braille']['enabled'] = not environment['braille']['enabled']
        if environment['braille']['enabled']: 
            environment['runtime']['outputManager'].presentText(environment, "braille enabled")
        else:
            environment['runtime']['outputManager'].presentText(environment, "braille disabled")
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

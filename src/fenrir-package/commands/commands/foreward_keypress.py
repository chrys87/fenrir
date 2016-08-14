#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['input']['keyForeward'] = True
        environment['runtime']['outputManager'].presentText(environment, 'Foreward next keypress', interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

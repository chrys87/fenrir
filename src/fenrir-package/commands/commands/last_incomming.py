#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newDelta'].strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", interrupt=True)
        else:    
           environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

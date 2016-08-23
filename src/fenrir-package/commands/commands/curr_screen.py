#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newContentText'].strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "screen is empty", interrupt=True)
        else:    
           environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newContentText'],interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

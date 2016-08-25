#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newContentText'].strip() == '':
            environment['runtime']['outputManager'].presentText(environment, "screen is empty", soundIcon='EmptyLine', interrupt=True)
        else:    
           environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newContentText'],interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

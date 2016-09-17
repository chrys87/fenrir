#!/bin/python
import fcntl
import sys
import termios


class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return 'clears the currently selected clipboard'     

    def run(self, environment):
        environment['commandBuffer']['currClipboard'] = -1
        del environment['commandBuffer']['clipboard'][:]
        environment['runtime']['outputManager'].presentText(environment, 'clipboard cleared', interrupt=True)
        return environment                
    def setCallback(self, callback):
        pass

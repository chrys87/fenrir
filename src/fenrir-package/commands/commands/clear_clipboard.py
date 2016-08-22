#!/bin/python
import fcntl
import sys
import termios


class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['commandBuffer']['currClipboard'] = -1
        del environment['commandBuffer']['clipboard'][:]
        environment['runtime']['outputManager'].presentText(environment, 'clipboard cleared', interrupt=True)
        return environment                
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

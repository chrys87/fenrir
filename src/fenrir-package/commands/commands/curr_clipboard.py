#!/bin/python
import fcntl
import sys
import termios


class command():
    def __init__(self):
        pass
    def run(self, environment):
        if len(environment['commandBuffer']['clipboard']) == 0:
            environment['runtime']['outputManager'].presentText(environment, 'clipboard empty', interrupt=True)
            return environment 
        environment['runtime']['outputManager'].presentText(environment, environment['commandBuffer']['clipboard'][environment['commandBuffer']['currClipboard']], interrupt=True)
        return environment                
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

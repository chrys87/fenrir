#!/bin/python
import fcntl
import sys
import termios
import time

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return 'pastes the text from the currently selected clipboard'        
    
    def run(self, environment):
        currClipboard = environment['commandBuffer']['currClipboard']
        if currClipboard < 0:
            environment['runtime']['outputManager'].presentText(environment, 'clipboard empty', interrupt=True)
            return environment
        with open("/dev/tty" + environment['screenData']['newTTY'], 'w') as fd:
            for c in environment['commandBuffer']['clipboard'][currClipboard]:
                fcntl.ioctl(fd, termios.TIOCSTI, c)
                time.sleep(0.02)
        return environment                
    def setCallback(self, callback):
        pass

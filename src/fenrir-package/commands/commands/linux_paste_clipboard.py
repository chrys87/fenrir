#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import fcntl
import termios
import time, sys

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'pastes the text from the currently selected clipboard'        
    
    def run(self, environment):
        currClipboard = environment['commandBuffer']['currClipboard']
        if currClipboard < 0:
            environment['runtime']['outputManager'].presentText(environment, 'clipboard empty', interrupt=True)
            return
        with open("/dev/tty" + environment['screenData']['newTTY'], 'w') as fd:
            for c in environment['commandBuffer']['clipboard'][currClipboard]:
                fcntl.ioctl(fd, termios.TIOCSTI, c)
                time.sleep(0.02)
              
    def setCallback(self, callback):
        pass

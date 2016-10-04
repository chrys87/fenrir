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
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'pastes the text from the currently selected clipboard'        
    
    def run(self):
        currClipboard = self.env['commandBuffer']['currClipboard']
        if currClipboard < 0:
            self.env['runtime']['outputManager'].presentText('clipboard empty', interrupt=True)
            return
        self.env['runtime']['outputManager'].presentText('paste clipboard', soundIcon='PasedClipboardOnScreen', interrupt=True)
        with open("/dev/tty" + self.env['screenData']['newTTY'], 'w') as fd:
            for c in self.env['commandBuffer']['clipboard'][currClipboard]:
                fcntl.ioctl(fd, termios.TIOCSTI, c)
                time.sleep(0.02)
              
    def setCallback(self, callback):
        pass

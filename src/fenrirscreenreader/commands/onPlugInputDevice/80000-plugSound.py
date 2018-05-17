#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import time

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.lastTime = time.time()
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No description found'         
    def run(self):
        if time.time() - self.lastTime > 2:
            self.env['runtime']['outputManager'].playSoundIcon(soundIcon = 'accept', interrupt=True)     
            lastTime = time.time()
    def setCallback(self, callback):
        pass

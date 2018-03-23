#!/bin/python
import time
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
    
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'     

    def run(self):
        print(time.time())         
    def setCallback(self, callback):
        pass
        

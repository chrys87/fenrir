#!/bin/python
import time
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import time
import datetime

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.lastTime = datetime.datetime.now()
        self.lastDateString = ''
        self.lastTimeString = ''        
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'     

    def run(self):
        self.env['runtime']['screenDriver'].getSessionInformation()                    
    def setCallback(self, callback):
        pass
        

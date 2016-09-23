#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class applicationManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getCurrentApplication(self):
        currApp = self.environment['screenData']['newApplication'].upper()
        if not currApp:
            currApp == 'DEFAULT' 
        if currApp == '':
            currApp == 'DEFAULT' 
    def getPrevApplication(self):
        prevApp = self.environment['screenData']['oldApplication'].upper()
        if not prevApp:
            prevApp == 'DEFAULT' 
        if prevApp == '':
            prevApp == 'DEFAULT' 
    def isApplicationChange(self):
        return self.environment['screenData']['oldApplication'] != self.environment['screenData']['newApplication']

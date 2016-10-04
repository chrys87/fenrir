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
        currApp = self.env['screenData']['newApplication'].upper()
        if not currApp:
            currApp == 'DEFAULT' 
        if currApp == '':
            currApp == 'DEFAULT'
        return currApp
    def getPrevApplication(self):
        prevApp = self.env['screenData']['oldApplication'].upper()
        if not prevApp:
            prevApp == 'DEFAULT' 
        if prevApp == '':
            prevApp == 'DEFAULT' 
        return prevApp
    def isApplicationChange(self):
        return self.env['screenData']['oldApplication'] != self.env['screenData']['newApplication']

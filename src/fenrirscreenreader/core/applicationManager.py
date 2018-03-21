#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class applicationManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getCurrentApplication(self):
        currApp = self.env['screen']['newApplication'].upper()
        if not currApp:
            currApp == 'DEFAULT' 
        if currApp == '':
            currApp == 'DEFAULT'
        return currApp
    def getPrevApplication(self):
        prevApp = self.env['screen']['oldApplication'].upper()
        if not prevApp:
            prevApp == 'DEFAULT' 
        if prevApp == '':
            prevApp == 'DEFAULT' 
        return prevApp
    def isApplicationChange(self):
        return self.env['screen']['oldApplication'] != self.env['screen']['newApplication']

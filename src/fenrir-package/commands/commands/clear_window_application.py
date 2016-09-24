#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'Turn off window mode for application'
    
    def run(self):
        if self.env['runtime']['cursorManager'].clearWindowForApplication():
            currApp = self.env['runtime']['applicationManager'].getCurrentApplication()    
            self.env['runtime']['outputManager'].presentText('Window Mode off for application ' + currApp, interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText("Not in window Mode", interrupt=True)
        
    def setCallback(self, callback):
        pass

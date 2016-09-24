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
        return 'set Window Mode, needs 2 marks '
    
    def run(self):
        if self.env['runtime']['cursorManager'].setWindowForApplication():
            currApp = self.env['runtime']['applicationManager'].getCurrentApplication()    
            self.env['runtime']['outputManager'].presentText('Window Mode on for application ' + currApp, interrupt=True)
            self.env['runtime']['cursorManager'].clearMarks()
        else:
            self.env['runtime']['outputManager'].presentText("Set window beginn and end marks", interrupt=True)
        
    def setCallback(self, callback):
        pass

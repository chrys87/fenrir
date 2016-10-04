#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        self.ID = '4'
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'remove Bookmark ' + self.ID        
    
    def run(self):
        currApp = self.env['runtime']['applicationManager'].getCurrentApplication()
        
        del self.env['commandBuffer']['bookMarks'][self.ID][currApp]

        self.env['runtime']['outputManager'].presentText('Bookmark ' + self.ID + " removed for application " + currApp, interrupt=True)

    def setCallback(self, callback):
        pass

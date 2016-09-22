#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        self.ID = '1'
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'remove Bookmark ' + self.ID        
    
    def run(self):
        currApp = ''
        try:
            currApp = str(self.env['screenData']['newApplication'][0])
        except:
            currApp = 'DEFAULT'   
        del self.env['commandBuffer']['bookMarks'][self.ID][currApp]

        self.env['runtime']['outputManager'].presentText('Bookmark ' + self.ID + " removed for application " + currApp, interrupt=True)

    def setCallback(self, callback):
        pass

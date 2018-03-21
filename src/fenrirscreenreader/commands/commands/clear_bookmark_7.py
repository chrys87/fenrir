#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        self.ID = '7'
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('remove Bookmark {0}').format(self.ID,)        
    
    def run(self):
        currApp = self.env['runtime']['applicationManager'].getCurrentApplication()

        del self.env['commandBuffer']['bookMarks'][self.ID][currApp]

        self.env['runtime']['outputManager'].presentText(_('Bookmark {0} removed for application {1}').format(self.ID, currApp), interrupt=True)

    def setCallback(self, callback):
        pass

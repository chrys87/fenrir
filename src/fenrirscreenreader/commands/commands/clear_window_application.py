#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('Turn off window mode for application')
    
    def run(self):
        if self.env['runtime']['cursorManager'].clearWindowForApplication():
            currApp = self.env['runtime']['applicationManager'].getCurrentApplication()    
            self.env['runtime']['outputManager'].presentText(_('Window Mode off for application {0}').format(currApp,), interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(_("Not in window Mode"), interrupt=True)
        
    def setCallback(self, callback):
        pass

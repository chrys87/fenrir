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
        return _('set Window Mode, needs 2 marks ')
    
    def run(self):
        if self.env['runtime']['cursorManager'].setWindowForApplication():
            currApp = self.env['runtime']['applicationManager'].getCurrentApplication()    
            self.env['runtime']['outputManager'].presentText(_('Window Mode on for application {0}').format(currApp), interrupt=True)
            self.env['runtime']['cursorManager'].clearMarks()
        else:
            self.env['runtime']['outputManager'].presentText(_("Set window begin and end marks"), interrupt=True)
        
    def setCallback(self, callback):
        pass

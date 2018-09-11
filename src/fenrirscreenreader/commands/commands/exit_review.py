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
        return _('exits review mode')        
    
    def run(self):
        if not self.env['runtime']['cursorManager'].isReviewMode():
            self.env['runtime']['outputManager'].presentText(_("Not in Review Mode"), interrupt=True)
            return  

        self.env['runtime']['cursorManager'].clearReviewCursor()
        self.env['runtime']['outputManager'].presentText(_("Exiting Review Mode"), interrupt=True)
   
    def setCallback(self, callback):
        pass

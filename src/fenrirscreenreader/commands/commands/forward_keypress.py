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
        return _('sends the following keypress to the terminal or application')        
    
    def run(self):
        self.env['input']['keyForeward'] = 3
        self.env['runtime']['outputManager'].presentText(_('Forward next keypress'), interrupt=True)

    def setCallback(self, callback):
        pass

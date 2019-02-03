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
        self.env['runtime']['vmenuManager'].togglelVMenuMode()
        return _('Exiting v menu mode.')
    def run(self):
        self.env['runtime']['vmenuManager'].togglelVMenuMode()
        self.env['runtime']['outputManager'].presentText( _('Entering v menu.'), interrupt=True)
    def setCallback(self, callback):
        pass

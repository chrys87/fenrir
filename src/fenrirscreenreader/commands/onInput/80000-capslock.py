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
        return 'No description found'         
    def run(self):
        if self.env['input']['oldCapsLock'] == self.env['input']['newCapsLock']:
            return
        if self.env['input']['newCapsLock']:
            self.env['runtime']['outputManager'].presentText(_("Capslock on"), interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(_("Capslock off"), interrupt=True)
        
    def setCallback(self, callback):
        pass

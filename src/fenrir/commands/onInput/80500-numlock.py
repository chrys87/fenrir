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
        return 'No description found'         
    def run(self):
        if self.env['input']['oldNumLock'] == self.env['input']['newNumLock']:
            return
        if self.env['input']['newNumLock']:
            self.env['runtime']['outputManager'].presentText("Numlock on", interrupt=False)
        else:
            self.env['runtime']['outputManager'].presentText("Numlock off", interrupt=False)
        
    def setCallback(self, callback):
        pass

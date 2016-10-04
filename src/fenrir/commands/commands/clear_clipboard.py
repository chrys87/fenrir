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
        return 'clears the currently selected clipboard'     

    def run(self):
        self.env['commandBuffer']['currClipboard'] = -1
        del self.env['commandBuffer']['clipboard'][:]
        self.env['runtime']['outputManager'].presentText('clipboard cleared', interrupt=True)
        return                
    def setCallback(self, callback):
        pass

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
        return 'removes marks from selected text'        
    
    def run(self):
        self.env['commandBuffer']['Marks']['1'] = None
        self.env['commandBuffer']['Marks']['2'] = None
        self.env['runtime']['outputManager'].presentText('Remove marks', interrupt=True)

    def setCallback(self, callback):
        pass

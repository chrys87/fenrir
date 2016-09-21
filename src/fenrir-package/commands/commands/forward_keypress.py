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
        return 'sends the following keypress to the terminal'        
    
    def run(self):
        self.env['input']['keyForeward'] = True
        self.env['runtime']['outputManager'].presentText('Foreward next keypress', interrupt=True)

    def setCallback(self, callback):
        pass

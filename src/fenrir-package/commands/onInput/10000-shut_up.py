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
        return ''               
    
    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'interruptOnKeyPress'):
            return 
        if self.env['screenData']['newTTY'] != self.env['screenData']['oldTTY']:
            return               

        self.env['runtime']['outputManager'].interruptOutput()

    def setCallback(self, callback):
        pass

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
        return 'No Description found'      

    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'autoReadIncomming'):
            return
        # is there something to read?
        if self.env['screenData']['newDelta'] == '':
            return            
        # dont read TTY change
        if self.env['screenData']['newTTY'] != self.env['screenData']['oldTTY']:
            return
        # its a cursor movement (experimental) - maybe also check current shortcut string?
        if abs(self.env['screenData']['newCursor']['x'] - self.env['screenData']['oldCursor']['x']) >= 1:
            if len(self.env['screenData']['newDelta']) <= 5:
                return          
    
        self.env['runtime']['outputManager'].presentText(self.env['screenData']['newDelta'], interrupt=False)

    def setCallback(self, callback):
        pass


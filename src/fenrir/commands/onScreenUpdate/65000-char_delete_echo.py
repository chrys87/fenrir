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
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'charDeleteEcho'):
            return
   
        # detect typing or chilling
        if self.env['screenData']['newCursor']['x'] >= self.env['screenData']['oldCursor']['x']:
            return 

        # More than just a deletion happend
        if self.env['screenData']['newDelta'].strip() != '':
            if self.env['screenData']['newDelta'] != self.env['screenData']['oldDelta']:
    	        return          
        # No deletion 
        if self.env['screenData']['newNegativeDelta'] == '':
            return
        # too much for a single backspace...
        if len(self.env['screenData']['newNegativeDelta']) >= 2:
            return           

        self.env['runtime']['outputManager'].presentText(self.env['screenData']['newNegativeDelta'], interrupt=True, ignorePunctuation=True, announceCapital=True)

    def setCallback(self, callback):
        pass


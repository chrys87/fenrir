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
        if self.environment['runtime']['screenManager'].isDelta():
            return
        # no deletion
        if not self.environment['runtime']['screenManager'].isNegativeDelta():
            return
        if self.env['runtime']['inputManager'].noKeyPressed():
            return              
        # too much for a single backspace...
        if len(self.env['screenData']['newNegativeDelta']) >= 2:
            return           

        self.env['runtime']['outputManager'].presentText(self.env['screenData']['newNegativeDelta'], interrupt=True, ignorePunctuation=True, announceCapital=True)

    def setCallback(self, callback):
        pass


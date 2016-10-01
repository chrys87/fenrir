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
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'charEcho'):
            return
        # detect deletion or chilling 
        if self.env['screenData']['newCursor']['x'] <= self.env['screenData']['oldCursor']['x']:
            return
        if self.env['runtime']['inputManager'].noKeyPressed():
            return              
        # is there any change?
        if self.env['screenData']['newDelta'] == '':
            return
        # big changes are no char (but the value is bigger than one maybe the differ needs longer than you can type, so a little strange random buffer for now)
        if len(self.env['screenData']['newDelta']) > 3:
            return        
        self.env['runtime']['outputManager'].presentText(self.env['screenData']['newDelta'], interrupt=True, ignorePunctuation=True, announceCapital=True)

    def setCallback(self, callback):
        pass


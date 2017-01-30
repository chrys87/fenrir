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
        if not self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'autoReadIncoming'):
            return
        # is there something to read?
        if self.env['screenData']['newDelta'] == '':
            return            

        # its a cursor movement (experimental) - maybe also check current shortcut string?
        if abs(self.env['screenData']['newCursor']['x'] - self.env['screenData']['oldCursor']['x']) >= 1:
            if len(self.env['screenData']['newDelta'].strip(' \n\t')) <= 2:
                return          

        self.env['runtime']['outputManager'].presentText(self.env['screenData']['newDelta'], interrupt=False, flush=False)

    def setCallback(self, callback):
        pass


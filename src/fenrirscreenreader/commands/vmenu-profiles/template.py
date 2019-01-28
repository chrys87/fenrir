#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        # example:
        # self.keyMakro = [[1,'KEY_CONTROL'],[300,'SLEEP'],[1,'KEY_O'],[10,'SLEEP'],[0,'KEY_O'], [10,'SLEEP'],[0,'KEY_CONTROL']]
        self.keyMakro = []
        self.byteMakro = []
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No description found'
    def run(self):
        if self.env['runtime']['inputManager'].getShortcutType() in ['KEY']:
            self.env['runtime']['inputManager'].sendKeys(self.keyMakro)
        if self.env['runtime']['inputManager'].getShortcutType() in ['BYTE']:
            self.env['runtime']['byteManager'].sendBytes(self.byteMakro)
    def setCallback(self, callback):
        pass

#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
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

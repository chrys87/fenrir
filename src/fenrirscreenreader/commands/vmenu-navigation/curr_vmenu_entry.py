#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('get current v menu entry')
    def run(self):
        text = self.env['runtime']['vmenuManager'].getCurrentEntry()
        self.env['runtime']['outputManager'].presentText(text, interrupt=True)
    def setCallback(self, callback):
        pass

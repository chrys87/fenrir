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
        return _('leave v menu submenu')
    def run(self):
        print('DEC LEVEL')
        try:
            self.env['runtime']['vmenuManager'].decLevel()
            text = self.env['runtime']['vmenuManager'].getCurrentEntry()
            self.env['runtime']['outputManager'].presentText(text, interrupt=True)
        except Exception as e:
            print(e)
    def setCallback(self, callback):
        pass

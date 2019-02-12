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
        self.keyMakro = [[1, 'KEY_LEFTCTRL'], [1, 'KEY_G'], [0.05,'sleep'] ,[0, 'KEY_G'], [0, 'KEY_LEFTCTRL']]
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No description found'         
    def run(self):
        self.env['runtime']['inputManager'].sendKeys(self.keyMakro)
    def setCallback(self, callback):
        pass




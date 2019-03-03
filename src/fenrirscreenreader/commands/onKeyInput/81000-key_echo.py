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
        return 'No description found'
    def run(self):
        if self.env['runtime']['helpManager'].isTutorialMode():
            self.env['runtime']['inputManager'].keyEcho(event)

    def setCallback(self, callback):
        pass

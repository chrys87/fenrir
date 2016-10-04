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
        self.env['commandBuffer']['Marks']['1']  = None
        self.env['commandBuffer']['Marks']['2']  = None

    def setCallback(self, callback):
        pass


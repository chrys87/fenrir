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
        return 'move review to bottom of screen'         

    def run(self):
        self.env['screenData']['newCursorReview'] = { 'x': 0, 'y':self.env['screenData']['lines'] -1}
        self.env['runtime']['outputManager'].presentText("Bottom", interrupt=True, flush=False)     

    def setCallback(self, callback):
        pass

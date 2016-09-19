#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):   
        pass
    def getDescription(self, environment):
        return 'move review to bottom of screen'         

    def run(self, environment):
        environment['screenData']['newCursorReview'] = { 'x': 0, 'y':environment['screenData']['lines']}
        environment['runtime']['outputManager'].presentText(environment, "Bottom", interrupt=True)     

    def setCallback(self, callback):
        pass

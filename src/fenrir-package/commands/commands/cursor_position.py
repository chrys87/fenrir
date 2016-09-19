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
        return 'displays the position of the review cursor'        

    def run(self, environment):
        # Prefer review cursor over text cursor
        if (environment['screenData']['newCursorReview'] != None):
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()

        environment['runtime']['outputManager'].presentText(environment, "line "+  str(cursorPos['y']+1) + " column "+  str(cursorPos['x']+1), interrupt=True)
   
    def setCallback(self, callback):
        pass

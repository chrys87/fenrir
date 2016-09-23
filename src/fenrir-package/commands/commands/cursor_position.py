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
        return 'displays the position of the review cursor'        

    def run(self):
        # Prefer review cursor over text cursor
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()

        self.env['runtime']['outputManager'].presentText("line "+  str(cursorPos['y']+1) + " column "+  str(cursorPos['x']+1), interrupt=True)
   
    def setCallback(self, callback):
        pass

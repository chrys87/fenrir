#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import os
import sys

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('displays the position of the review cursor and current TTY')        

    def run(self):
        # Prefer review cursor over text cursor
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()

        self.env['runtime']['outputManager'].presentText(_("line {0}, column {1}, " + str(os.ttyname(sys.stdout.fileno()))[5:].replace("/", "")).format(cursorPos['y']+1, cursorPos['x']+1), interrupt=True)
   
    def setCallback(self, callback):
        pass

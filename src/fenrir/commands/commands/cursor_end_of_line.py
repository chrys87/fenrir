#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import line_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'read to end of line, use review cursor if you are in reviewmode, otherwhise use text cursor'        
    
    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()

        x, y, currLine = \
          line_utils.getCurrentLine(cursorPos['x'], cursorPos['y'], self.env['screenData']['newContentText'])
        
        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(currLine[cursorPos['x']], interrupt=True) 
        self.env['runtime']['outputManager'].announceActiveCursor()            
    def setCallback(self, callback):
        pass


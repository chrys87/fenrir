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
        return 'shows the indention level for the current line'        

    def run(self):
        # Prefer review cursor over text cursor

        if self.env['screenData']['newCursorReview']:
            cursorPos = self.env['screenData']['newCursorReview'].copy()
        else:
            cursorPos = self.env['screenData']['newCursor'].copy()
        x, y, currLine = \
          line_utils.getCurrentLine(cursorPos['x'], cursorPos['y'], self.env['screenData']['newContentText'])
        
        if currLine.strip(" \t\n") == '':
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:        
            self.env['runtime']['outputManager'].presentText("indent "+  str(len(currLine) - len(currLine.lstrip())), interrupt=True)

    def setCallback(self, callback):
        pass

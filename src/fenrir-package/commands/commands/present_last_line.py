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
        return 'current line'        
    
    def run(self):
        x, y, lastLine = \
          line_utils.getCurrentLine(0, self.env['screenData']['lines'] -1, self.env['screenData']['newContentText'])

        if lastLine.strip(" \t\n") == '':
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(lastLine, interrupt=True) 
    def setCallback(self, callback):
        pass


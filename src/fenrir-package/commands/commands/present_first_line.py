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
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'present first line'        
    
    def run(self, environment):
        x, y, firstLine = \
          line_utils.getCurrentLine(0, 0, environment['screenData']['newContentText'])
        
        if firstLine.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", soundIcon='EmptyLine', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, firstLine, interrupt=True) 
    def setCallback(self, callback):
        pass


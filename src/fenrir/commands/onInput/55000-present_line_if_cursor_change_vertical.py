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
        return ''        
    
    def run(self):
        if self.env['runtime']['inputManager'].noKeyPressed():
            return     
        if self.env['runtime']['screenManager'].isScreenChange():
            return
        if self.env['runtime']['screenManager'].isDelta():
            return    
        # is a vertical change?
        if not self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return   
       
        x, y, currLine = line_utils.getCurrentLine(self.env['screenData']['newCursor']['x'], self.env['screenData']['newCursor']['y'], self.env['screenData']['newContentText'])

        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(currLine, interrupt=True)
 
    def setCallback(self, callback):
        pass


#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import line_utils
from utils import word_utils

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
        if not self.env['runtime']['settingsManager'].getSettingAsBool('focus', 'cursor'):
            return      
        if self.env['runtime']['screenManager'].isScreenChange():
            return        
        # this leads to problems in vim -> status line change -> no announcement, so we do check the lengh as hack
        if self.env['runtime']['screenManager'].isDelta():
            if len(self.env['screen']['newDelta']) > 4:  
                return
            
        # is a vertical change?
        if not self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return   
       
        x, y, currLine = line_utils.getCurrentLine(self.env['screen']['newCursor']['x'], self.env['screen']['newCursor']['y'], self.env['screen']['newContentText'])

        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True, flush=False)
        else:
            self.env['runtime']['outputManager'].presentText(currLine, interrupt=True, flush=False)
 
    def setCallback(self, callback):
        pass


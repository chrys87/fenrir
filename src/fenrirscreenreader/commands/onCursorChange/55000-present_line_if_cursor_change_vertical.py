#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import line_utils
from fenrirscreenreader.utils import word_utils

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
            return
            
        # is a vertical change?
        if not self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return   
       
        x, y, currLine = line_utils.getCurrentLine(self.env['screen']['newCursor']['x'], self.env['screen']['newCursor']['y'], self.env['screen']['newContentText'])

        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True, flush=False)
        else:
            if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'autoPresentIndent'):
                if oldIndent < newIndent: self.env['runtime']['outputManager'].presentText('indented ' + str(oldIndent - newIndent), interrupt=True, flush=False)
                if oldIndent > newIndent: self.env['runtime']['outputManager'].presentText('outdented ' + str(newIndent - oldIndent), interrupt=True, flush=False)
            self.env['runtime']['outputManager'].presentText(currLine, interrupt=True, flush=False)
 
    def setCallback(self, callback):
        pass


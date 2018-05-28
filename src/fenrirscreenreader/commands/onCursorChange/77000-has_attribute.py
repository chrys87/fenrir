#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import screen_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return _('Reads attributes of current cursor position')         
    def run(self):
        # is it enabled?    
        if not self.env['runtime']['settingsManager'].getSettingAsBool('general', 'hasAttributes'):
            return    
        # is a vertical change?
        if not (self.env['runtime']['cursorManager'].isCursorVerticalMove() or\
          self.env['runtime']['cursorManager'].isCursorHorizontalMove()):
            return       

        cursorPos = self.env['screen']['newCursor']
        
        if not self.env['runtime']['attributeManager'].hasAttributes(cursorPos):
            return
        self.env['runtime']['outputManager'].presentText('has attribute', soundIcon='HasAttributes', interrupt=False)
    def setCallback(self, callback):
        pass

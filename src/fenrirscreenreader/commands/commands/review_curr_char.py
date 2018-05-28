#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import char_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('presents the current character.')        
    
    def run(self):
        self.env['runtime']['cursorManager'].enterReviewModeCurrTextCursor()

        self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], currChar = \
          char_utils.getCurrentChar(self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], self.env['screen']['newContentText'])
        
        self.env['runtime']['outputManager'].presentText(currChar ,interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False)
        # is has attribute it enabled?    
        if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'hasAttributes'):
            cursorPos = self.env['screen']['newCursorReview']
            
            if not self.env['runtime']['attributeManager'].hasAttributes(cursorPos):
                return
            self.env['runtime']['outputManager'].presentText('has attribute', soundIcon='HasAttributes', interrupt=False)        
  
    def setCallback(self, callback):
        pass

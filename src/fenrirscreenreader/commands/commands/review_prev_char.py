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
        return _('moves review to the previous character ')        
    
    def run(self):
        self.env['screen']['oldCursorReview'] = self.env['screen']['newCursorReview']
        if not self.env['screen']['newCursorReview']:
            self.env['screen']['newCursorReview'] = self.env['screen']['newCursor'].copy()

        self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], prevChar, endOfScreen, lineBreak = \
          char_utils.getPrevChar(self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], self.env['screen']['newContentText'])
        
        self.env['runtime']['outputManager'].presentText(prevChar, interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False)
        if endOfScreen:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'endOfScreen'):        
                self.env['runtime']['outputManager'].presentText(_('end of screen'), interrupt=True, soundIcon='EndOfScreen')                 
        if lineBreak:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'lineBreak'):        
                self.env['runtime']['outputManager'].presentText(_('line break'), interrupt=False, soundIcon='EndOfLine')  
        # is has attribute it enabled?    
        if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'hasAttributes'):
            cursorPos = self.env['screen']['newCursorReview']
            
            if not self.env['runtime']['attributeManager'].hasAttributes(cursorPos):
                return
            self.env['runtime']['outputManager'].presentText('has attribute', soundIcon='HasAttributes', interrupt=False)                      
    def setCallback(self, callback):
        pass

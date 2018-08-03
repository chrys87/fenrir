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
        return _('Move review to the character in the line above the current position')        

    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], upChar, endOfScreen = \
          char_utils.getUpChar(self.env['screen']['newCursorReview']['x'],self.env['screen']['newCursorReview']['y'], self.env['screen']['newContentText'])
        self.env['runtime']['outputManager'].presentText(upChar ,interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False) 
        if endOfScreen:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'endOfScreen'):        
                self.env['runtime']['outputManager'].presentText(_('end of screen'), interrupt=True, soundIcon='EndOfScreen')                 
        if lineBreak:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'lineBreak'):        
                self.env['runtime']['outputManager'].presentText(_('line break'), interrupt=False, soundIcon='EndOfLine')    
    def setCallback(self, callback):
        pass

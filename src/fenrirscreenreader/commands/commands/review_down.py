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
        return _('Move review to the character below the current position')        

    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], downChar, endOfScreen = \
          char_utils.getDownChar(self.env['screen']['newCursorReview']['x'],self.env['screen']['newCursorReview']['y'], self.env['screen']['newContentText'])
        self.env['runtime']['outputManager'].presentText(downChar ,interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False)
        if endOfScreen:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'endOfScreen'):        
                self.env['runtime']['outputManager'].presentText(_('end of screen'), interrupt=True, soundIcon='EndOfScreen')                     
    def setCallback(self, callback):
        pass

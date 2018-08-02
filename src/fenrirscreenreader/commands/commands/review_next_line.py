#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import line_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('moves review to the next line ')        
    
    def run(self):
        self.env['screen']['oldCursorReview'] = self.env['screen']['newCursorReview']
        if not self.env['screen']['newCursorReview']:
            self.env['screen']['newCursorReview'] = self.env['screen']['newCursor'].copy()

        self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], nextLine, endOfScreen = \
          line_utils.getNextLine(self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], self.env['screen']['newContentText'])
        
        if nextLine.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True, flush=False)
        else:
            self.env['runtime']['outputManager'].presentText(nextLine, interrupt=True, flush=False)
        if endOfScreen:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'endOfScreen'):        
                self.env['runtime']['outputManager'].presentText(_('end of screen'), interrupt=True, soundIcon='EndOfScreen')                 
    def setCallback(self, callback):
        pass

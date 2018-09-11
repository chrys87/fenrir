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
        return _('Presents the indentation level for the current line')        

    def run(self):
        # Prefer review cursor over text cursor

        if self.env['screen']['newCursorReview']:
            cursorPos = self.env['screen']['newCursorReview'].copy()
        else:
            cursorPos = self.env['screen']['newCursor'].copy()
        x, y, currLine = \
          line_utils.getCurrentLine(cursorPos['x'], cursorPos['y'], self.env['screen']['newContentText'])
        
        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True)
        else:        
            self.env['runtime']['outputManager'].presentText(_("indent {0}").format(len(currLine) - len(currLine.lstrip())), interrupt=True)

    def setCallback(self, callback):
        pass

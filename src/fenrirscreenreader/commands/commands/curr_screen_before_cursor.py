#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import mark_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('Reads from the top of the screen to the cursor position')        

    def run(self):
        # Prefer review cursor over text cursor
        if self.env['screen']['newCursorReview']:
            cursorPos = self.env['screen']['newCursorReview'].copy()
        else:
            cursorPos = self.env['screen']['newCursor'].copy()

        textBeforeCursor = mark_utils.getTextBeforeMark(cursorPos, self.env['screen']['newContentText'])

        if textBeforeCursor.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(textBeforeCursor, interrupt=True)
   
    def setCallback(self, callback):
        pass


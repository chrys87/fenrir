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
        return _('reads from the cursor to the bottom of the screen')        

    def run(self):
        # Prefer review cursor over text cursor
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()

        textAfterCursor = mark_utils.getTextAfterMark(cursorPos, self.env['screen']['newContentText'])

        if textAfterCursor.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(textAfterCursor, interrupt=True)

    def setCallback(self, callback):
        pass

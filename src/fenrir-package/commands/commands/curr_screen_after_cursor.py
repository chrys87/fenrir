#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import mark_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'reads from the cursor to the bottom of the screen'        

    def run(self):
        # Prefer review cursor over text cursor
        if self.env['screenData']['newCursorReview']:
            cursorPos = self.env['screenData']['newCursorReview'].copy()
        else:
            cursorPos = self.env['screenData']['newCursor'].copy()

        textAfterCursor = mark_utils.getTextAfterMark(cursorPos, self.env['screenData']['newContentText'])

        if textAfterCursor.strip(" \t\n") == '':
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(textAfterCursor, interrupt=True)

    def setCallback(self, callback):
        pass

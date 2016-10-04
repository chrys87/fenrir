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
        return 'Reads from the top of the screen to the cursor position'        

    def run(self):
        # Prefer review cursor over text cursor
        if self.env['screenData']['newCursorReview']:
            cursorPos = self.env['screenData']['newCursorReview'].copy()
        else:
            cursorPos = self.env['screenData']['newCursor'].copy()

        textBeforeCursor = mark_utils.getTextBeforeMark(cursorPos, self.env['screenData']['newContentText'])

        if textBeforeCursor.isspace():
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(textBeforeCursor, interrupt=True)
   
    def setCallback(self, callback):
        pass


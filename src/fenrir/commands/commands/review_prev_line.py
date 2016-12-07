#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import line_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'moves review to the previous line and presents it'        

    def run(self):
        self.env['runtime']['cursorManager'].enterReviewModeCurrTextCursor()

        self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], prevLine, endOfScreen = \
          line_utils.getPrevLine(self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], self.env['screenData']['newContentText'])
        
        if prevLine.isspace():
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(prevLine, interrupt=True)
        if endOfScreen:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'endOfScreen'):        
                self.env['runtime']['outputManager'].presentText('end of screen' ,interrupt=False, soundIcon='EndOfScreen')                 

    def setCallback(self, callback):
        pass

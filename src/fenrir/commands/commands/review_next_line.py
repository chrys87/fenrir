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
        return 'moves review to the next line and presents it'        
    
    def run(self):
        self.env['screenData']['oldCursorReview'] = self.env['screenData']['newCursorReview']
        if not self.env['screenData']['newCursorReview']:
            self.env['screenData']['newCursorReview'] = self.env['screenData']['newCursor'].copy()

        self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], nextLine, endOfScreen = \
          line_utils.getNextLine(self.env['screenData']['newCursorReview']['x'], self.env['screenData']['newCursorReview']['y'], self.env['screenData']['newContentText'])
        
        if nextLine.isspace():
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(nextLine, interrupt=True)
        if endOfScreen:
            if self.env['runtime']['settingsManager'].getSettingAsBool('review', 'endOfScreen'):        
                self.env['runtime']['outputManager'].presentText('end of screen' ,interrupt=False, soundIcon='EndOfScreen')                 
    def setCallback(self, callback):
        pass

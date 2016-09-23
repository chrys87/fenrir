#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class cursorManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def clearMarks(self):
        self.env['commandBuffer']['Marks']['1'] = None
        self.env['commandBuffer']['Marks']['2'] = None
    def setMark(self):
      if not self.env['commandBuffer']['Marks']['1']:
            self.env['commandBuffer']['Marks']['1'] = self.env['screenData']['newCursorReview'].copy()
        else:
            self.env['commandBuffer']['Marks']['2'] = self.env['screenData']['newCursorReview'].copy()
    def getReviewOrTextCursor(self):
        if self.env['screenData']['newCursorReview']:
            return = self.env['screenData']['newCursorReview'].copy()
        else:
            return = self.env['screenData']['newCursor'].copy()
    def clearReviewCursor(self):
        self.env['screenData']['oldCursorReview'] = None
        self.env['screenData']['newCursorReview'] = None
    def isReviewMode(self):
        return self.env['screenData']['newCursorReview'] != None
        

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
    def isMarkSet(self):
        return self.env['commandBuffer']['Marks']['1'] != None
    def isSingleMark(self):
        return self.env['commandBuffer']['Marks']['1'] != None and \
          self.env['commandBuffer']['Marks']['2'] == None
    def isMultibleMark(self):
        return self.env['commandBuffer']['Marks']['1'] != None and \
          self.env['commandBuffer']['Marks']['2'] != None        
    def setMark(self):
        currCursor = None
        if self.env['screenData']['newCursorReview']:
            currCursor = self.env['screenData']['newCursorReview'].copy()
        else:
            currCursor = self.env['screenData']['newCursor'].copy()
        if not self.env['commandBuffer']['Marks']['1']:
            self.env['commandBuffer']['Marks']['1'] = currCursor.copy()
            return 1
        else:
            self.env['commandBuffer']['Marks']['2'] = currCursor.copy()
            return 2
        return 0
    def getReviewOrTextCursor(self):
        if self.env['screenData']['newCursorReview']:
            return self.env['screenData']['newCursorReview'].copy()
        else:
            return self.env['screenData']['newCursor'].copy()
    def clearReviewCursor(self):
        if not self.isReviewMode():
            return
        self.env['screenData']['oldCursorReview'] = None
        self.env['screenData']['newCursorReview'] = None
        
    def isReviewMode(self):
        return self.env['screenData']['newCursorReview'] != None
    def enterReviewModeCurrTextCursor(self, overwrite=False):
        if self.isReviewMode() and not overwrite:
            return
        self.env['screenData']['oldCursorReview'] = self.env['screenData']['newCursorReview']
        if not self.env['screenData']['newCursorReview']:
            self.env['screenData']['newCursorReview'] = self.env['screenData']['newCursor'].copy()
    def setReviewCursorPosition(self, x, y):
        if not self.isReviewMode():
            self.enterReviewModeCurrTextCursor()
        self.env['screenData']['oldCursorReview'] = self.env['screenData']['newCursorReview']
        self.env['screenData']['newCursorReview']['x'] = x
        self.env['screenData']['newCursorReview']['y'] = y
    def isApplicationWindowSet(self):
        try:
            currApp = self.env['runtime']['applicationManager'].getCurrentApplication()
            if self.env['commandBuffer']['windowArea'][currApp]['1'] != None:
                return True
        except:
            pass
        return False
    def setWindowForApplication(self):
        if not self.env['commandBuffer']['Marks']['1']:
            return False
        if not self.env['commandBuffer']['Marks']['2']:
            return False
        currApp = self.env['runtime']['applicationManager'].getCurrentApplication()
        self.env['commandBuffer']['windowArea'][currApp] = {}
        
        if self.env['commandBuffer']['Marks']['1']['x'] * self.env['commandBuffer']['Marks']['1']['y'] <= \
          self.env['commandBuffer']['Marks']['2']['x'] * self.env['commandBuffer']['Marks']['2']['y']:
            self.env['commandBuffer']['windowArea'][currApp]['1'] = self.env['commandBuffer']['Marks']['1'].copy()
            self.env['commandBuffer']['windowArea'][currApp]['2'] = self.env['commandBuffer']['Marks']['2'].copy()
        else:
            self.env['commandBuffer']['windowArea'][currApp]['1'] = self.env['commandBuffer']['Marks']['2'].copy()
            self.env['commandBuffer']['windowArea'][currApp]['2'] = self.env['commandBuffer']['Marks']['1'].copy()  
        return True   
    def clearWindowForApplication(self):
        currApp = self.env['runtime']['applicationManager'].getCurrentApplication()
        try:
            del self.env['commandBuffer']['windowArea'][currApp]
        except:
            return False
        return True                                 

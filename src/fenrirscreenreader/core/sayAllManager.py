#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import word_utils

class sayAllManager():
    def __init__(self):
        self.isActive = False
        self.isActiveLock = None
        self.clipboardContent = ''
    def initialize(self, environment):
        self.env = environment  
    def resetClipboardContent(self):
        self.clipboardContent = ''
    def addToClipboardContent(self, text):
        self.clipboardContent += text
    def getClipboardContent(self):
        return self.clipboardContent
    def shutdown(self):
        if self.isSayAllActive():
            self.stop()
    def setIsActive(self, isActive):
        self.isActive = isActive
    def start(self):
        self.setIsActive(True)
        self.env['runtime']['debug'].writeDebugOut('sayAllManager: start say all' ,debug.debugLevel.INFO)
        self.resetClipboardContent()
        print('start say all')
    def isSayAllActive(self):
        return self.isActive
    def sayAllWorker(self):
        nextWord = ''
        try:
            if self.env['screen']['newCursorReview'] == None:
                self.env['screen']['newCursorReview'] = self.env['runtime']['cursorManager'].createCursor(0, 0)

            self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], nextWord, endOfScreen, lineBreak = \
              word_utils.getNextWord(self.env['screen']['newCursorReview']['x'], self.env['screen']['newCursorReview']['y'], self.env['screen']['newContentText'])
        except Exception as e:
            print(e)
        print(nextWord,'word')
        self.env['runtime']['outputManager'].presentText(nextWord, interrupt=True, flush=False)
    def stop(self):
        self.setIsActive(False)
        self.env['runtime']['debug'].writeDebugOut('sayAllManager: stop say all' ,debug.debugLevel.INFO)
        print('stop say all')
    def gotoNextPage(self):
        pass

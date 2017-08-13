#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No description found'         
    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        attributes = self.env['screen']['newContentAttrib'][cursorPos['x']][cursorPos['y']]
        attributeFormatString = self.env['runtime']['settingsManager'].getSetting('general', 'attributeFormatString')
        attributeFormatString = self.env['runtime']['screenManager'].formatAttributes(attributeFormatString)
        self.env['runtime']['outputManager'].presentText(attributeFormatString, soundIcon='', interrupt=True)
    def setCallback(self, callback):
        pass

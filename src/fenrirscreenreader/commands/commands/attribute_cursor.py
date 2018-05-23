#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import screen_utils

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
        attributes = screen_utils.splitEvery(self.env['screen']['newContentAttrib'], self.env['screen']['columns'])
        attributes = self.env['screen']['newContentAttrib'][cursorPos['y']][cursorPos['x']]
        attributeFormatString = self.env['runtime']['settingsManager'].getSetting('general', 'attributeFormatString')
        attributeFormatString = self.env['runtime']['screenManager'].formatAttributes(attributes, attributeFormatString)
        self.env['runtime']['outputManager'].presentText(attributeFormatString, soundIcon='', interrupt=True)
    def setCallback(self, callback):
        pass

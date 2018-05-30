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
        return _('Reads attributes of current cursor position')         
    def run(self):
        cursorPos = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        try:
            attributes = self.env['runtime']['attributeManager'].getAttributeByXY( cursorPos['x'], cursorPos['y'])
        except Exception as e:
            print(e)        
        attributeFormatString = self.env['runtime']['settingsManager'].getSetting('general', 'attributeFormatString')
        attributeFormatString = self.env['runtime']['attributeManager'].formatAttributes(attributes, attributeFormatString)
        
        self.env['runtime']['outputManager'].presentText(attributeFormatString, soundIcon='', interrupt=True)
    def setCallback(self, callback):
        pass

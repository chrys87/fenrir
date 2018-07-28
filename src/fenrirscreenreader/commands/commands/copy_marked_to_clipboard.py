#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import mark_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('copies marked text to the currently selected clipboard')    
    
    def run(self):
        if not self.env['commandBuffer']['Marks']['1']:
            self.env['runtime']['outputManager'].presentText(_("One or two marks are needed"), interrupt=True)
            return
        if not self.env['commandBuffer']['Marks']['2']:
            self.env['runtime']['cursorManager'].setMark()

        # use the last first and the last setted mark as range
        startMark = self.env['commandBuffer']['Marks']['1'].copy()
        endMark = self.env['commandBuffer']['Marks']['2'].copy()         
        
        marked = mark_utils.getTextBetweenMarks(startMark, endMark, self.env['screen']['newContentText'])
        self.env['runtime']['memoryManager'].addValueToFirstIndex('clipboardHistory', marked)
        # reset marks
        self.env['runtime']['cursorManager'].clearMarks()      

        self.env['runtime']['outputManager'].presentText(marked, soundIcon='CopyToClipboard', interrupt=True)

    def setCallback(self, callback):
        pass

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
        return _('Presents the currently selected text that will be copied to the clipboard')        
    
    def run(self):
        if not (self.env['commandBuffer']['Marks']['1'] and \
          self.env['commandBuffer']['Marks']['2']):
            self.env['runtime']['outputManager'].presentText(_("please set begin and endmark"), interrupt=True)
            return

        # use the last first and the last setted mark as range
        startMark = self.env['commandBuffer']['Marks']['1'].copy()
        endMark = self.env['commandBuffer']['Marks']['2'].copy() 

        marked = mark_utils.getTextBetweenMarks(startMark, endMark, self.env['screen']['newContentText'])

        if marked.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(marked, interrupt=True)
    
    def setCallback(self, callback):
        pass

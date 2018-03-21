#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import line_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('current line')        
    
    def run(self):
        x, y, lastLine = \
          line_utils.getCurrentLine(0, self.env['screen']['lines'] -1, self.env['screen']['newContentText'])

        if lastLine.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(lastLine, interrupt=True) 
    def setCallback(self, callback):
        pass


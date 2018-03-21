#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('places marks to select text to copy to the clipboard')        
    
    def run(self):
        if not self.env['runtime']['cursorManager'].isReviewMode():
            self.env['runtime']['outputManager'].presentText(_('no review cursor'), interrupt=True)
            return

        currMark = self.env['runtime']['cursorManager'].setMark()
        if currMark == 1:
            self.env['runtime']['outputManager'].presentText(_('set mark'), soundIcon='PlaceStartMark', interrupt=True)
        elif currMark == 2:
            self.env['runtime']['outputManager'].presentText(_('set mark'),soundIcon='PlaceEndMark', interrupt=True)
    def setCallback(self, callback):
        pass

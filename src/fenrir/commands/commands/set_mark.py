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
        return 'places marks to select text to copy to the clipboard'        
    
    def run(self):
        if not self.env['runtime']['cursorManager'].isReviewMode():
            self.env['runtime']['outputManager'].presentText('no review cursor', interrupt=True)
            return

        self.env['runtime']['cursorManager'].setMark()
        self.env['runtime']['outputManager'].presentText('set mark', interrupt=True)
 
    def setCallback(self, callback):
        pass

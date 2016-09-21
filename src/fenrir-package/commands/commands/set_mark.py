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
        if not self.env['screenData']['newCursorReview']:
            self.env['runtime']['outputManager'].presentText('no review cursor', interrupt=True)
            return

        if not self.env['commandBuffer']['Marks']['1']:
            self.env['commandBuffer']['Marks']['1'] = self.env['screenData']['newCursorReview'].copy()
        else:
            self.env['commandBuffer']['Marks']['2'] = self.env['screenData']['newCursorReview'].copy()

        self.env['runtime']['outputManager'].presentText('set mark', interrupt=True)
 
    def setCallback(self, callback):
        pass

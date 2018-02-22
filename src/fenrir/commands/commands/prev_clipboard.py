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
        return _('selects the previous clipboard')        

    def run(self):
        if len(self.env['commandBuffer']['clipboard']) == 0:
            self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
            return 
        self.env['commandBuffer']['currClipboard'] -= 1
        if self.env['commandBuffer']['currClipboard'] < 0:
            self.env['commandBuffer']['currClipboard'] = len(self.env['commandBuffer']['clipboard']) -1
            self.env['runtime']['outputManager'].presentText(_('Last clipboard '), interrupt=True)            
            self.env['runtime']['outputManager'].presentText(self.env['commandBuffer']['clipboard'][self.env['commandBuffer']['currClipboard']], interrupt=False)            
        else:
            self.env['runtime']['outputManager'].presentText(self.env['commandBuffer']['clipboard'][self.env['commandBuffer']['currClipboard']], interrupt=True)
              
    def setCallback(self, callback):
        pass

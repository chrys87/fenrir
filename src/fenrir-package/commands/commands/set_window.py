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
        return 'set Window Mode, needs 2 marks '
    
    def run(self):
        if not self.env['commandBuffer']['Marks']['1']:
            self.env['runtime']['outputManager'].presentText("No Mark found", interrupt=True)
            return
        if not self.env['commandBuffer']['Marks']['2']:
            self.env['runtime']['outputManager'].presentText("to few makrs found", interrupt=True)
            return            
        currApp = self.env['runtime']['applicationManager'].getCurrentApplication()
        self.env['commandBuffer']['windowArea'][currApp] = {}
        
        if self.env['commandBuffer']['Marks']['1']['x'] * self.env['commandBuffer']['Marks']['1']['y'] <= \
          self.env['commandBuffer']['Marks']['2']['x'] * self.env['commandBuffer']['Marks']['2']['y']:
            self.env['commandBuffer']['windowArea'][currApp]['1'] = self.env['commandBuffer']['Marks']['1'].copy()
            self.env['commandBuffer']['windowArea'][currApp]['2'] = self.env['commandBuffer']['Marks']['2'].copy()
        else:
            self.env['commandBuffer']['windowArea'][currApp]['1'] = self.env['commandBuffer']['Marks']['2'].copy()
            self.env['commandBuffer']['windowArea'][currApp]['2'] = self.env['commandBuffer']['Marks']['1'].copy()
        
        self.env['runtime']['outputManager'].presentText('Window Mode  set for application ' + currApp, interrupt=True)
        self.env['commandBuffer']['Marks']['1'] = None
        self.env['commandBuffer']['Marks']['2'] = None
    def setCallback(self, callback):
        pass

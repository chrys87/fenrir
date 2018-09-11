#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        self.ID = '3'
    def initialize(self, environment):
        self.env = environment
        self.env['commandBuffer']['bookMarks'][self.ID] = {}
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('set Bookmark {0}').format(self.ID,)        
    
    def run(self):
        if not self.env['commandBuffer']['Marks']['1']:
            self.env['runtime']['outputManager'].presentText(_("No mark found"), interrupt=True)
            return
        currApp = self.env['runtime']['applicationManager'].getCurrentApplication()
        self.env['commandBuffer']['bookMarks'][self.ID][currApp] = {}
        
        self.env['commandBuffer']['bookMarks'][self.ID][currApp]['1'] = self.env['commandBuffer']['Marks']['1'].copy()
        if self.env['commandBuffer']['Marks']['2']:
            self.env['commandBuffer']['bookMarks'][self.ID][currApp]['2'] = self.env['commandBuffer']['Marks']['2'].copy()
        else:
            self.env['commandBuffer']['bookMarks'][self.ID][currApp]['2'] = None
        self.env['runtime']['outputManager'].presentText(_('Bookmark {0} set for application {1}').format(self.ID, currApp), interrupt=True)
        self.env['commandBuffer']['Marks']['1'] = None
        self.env['commandBuffer']['Marks']['2'] = None
    def setCallback(self, callback):
        pass

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
        return ''               
    
    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'interruptOnKeyPress'):
            return
        if self.env['runtime']['screenManager'].isScreenChange():
            return
        # if the filter is set
        #if self.env['runtime']['settingsManager'].getSetting('keyboard', 'interruptOnKeyPressFilter').strip() != '':            
        #    filterList = self.env['runtime']['settingsManager'].getSetting('keyboard', 'interruptOnKeyPressFilter').split(',')
        #    for currInput in self.env['input']['currInput']:
        #        if not currInput in filterList:
        #            return                                                  
        self.env['runtime']['outputManager'].interruptOutput()

    def setCallback(self, callback):
        pass

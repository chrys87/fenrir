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
        return ''               
    
    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'interruptOnKeyPress'):
            return     
        if self.env['runtime']['inputManager'].noKeyPressed():
            return        
        if len(self.env['input']['prevDeepestInput']) > len(self.env['input']['currInput']):
            return 
        if len(self.env['input']['currInput']) != 1:
            return
        # if the filter is set
        if self.env['runtime']['settingsManager'].getSetting('keyboard', 'interruptOnKeyPressFilter').strip() != '':            
            if not self.env['input']['currInput'][0] in self.env['runtime']['settingsManager'].getSetting('keyboard', 'interruptOnKeyPressFilter').split(','):
                return                                        
        if self.env['runtime']['screenManager'].isScreenChange():
            return               
        self.env['runtime']['outputManager'].interruptOutput()

    def setCallback(self, callback):
        pass

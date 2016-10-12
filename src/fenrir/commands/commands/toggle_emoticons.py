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
        return 'enables or disables announcement of emoticons insteed of chars'        
    
    def run(self):
        self.env['runtime']['settingsManager'].setSetting('general', 'emoticons', str(not self.env['runtime']['settingsManager'].getSettingAsBool('general', 'emoticons')))   
        if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'emoticons'): 
            self.env['runtime']['outputManager'].presentText("emoticons enabled", soundIcon='', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText("emoticons disabled", soundIcon='', interrupt=True)                          
    
    def setCallback(self, callback):
        pass

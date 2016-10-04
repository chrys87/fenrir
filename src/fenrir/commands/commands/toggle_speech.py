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
        return 'enables or disables speech'        
    
    def run(self):
        if self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'enabled'): 
            self.env['runtime']['outputManager'].presentText("speech disabled", soundIcon='SpeechOff', interrupt=True)
        self.env['runtime']['settingsManager'].setSetting('speech', 'enabled', str(not self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'enabled')))   
        if self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'enabled'): 
            self.env['runtime']['outputManager'].presentText("speech enabled", soundIcon='SpeechOn', interrupt=True)                 

    def setCallback(self, callback):
        pass

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
        return _('enables or disables sound')        

    def run(self):
        if self.env['runtime']['settingsManager'].getSettingAsBool('sound', 'enabled'): 
            self.env['runtime']['outputManager'].presentText(_('sound disabled'), soundIcon='SoundOff', interrupt=True)
        self.env['runtime']['settingsManager'].setSetting('sound', 'enabled', str(not self.env['runtime']['settingsManager'].getSettingAsBool('sound', 'enabled')))   
        if self.env['runtime']['settingsManager'].getSettingAsBool('sound', 'enabled'): 
            self.env['runtime']['outputManager'].presentText(_('sound enabled'), soundIcon='SoundOn', interrupt=True)                 
  
    def setCallback(self, callback):
        pass

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
        return _('enables or disables the barrier mode')        
    
    def run(self):
        self.env['runtime']['settingsManager'].setSetting('barrier', 'enabled', str(not self.env['runtime']['settingsManager'].getSettingAsBool('barrier', 'enabled')))
        if self.env['runtime']['settingsManager'].getSettingAsBool('barrier', 'enabled'): 
            self.env['runtime']['outputManager'].presentText(_("barrier mode enabled"), soundIcon='', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(_("barrier mode disabled"), soundIcon='', interrupt=True)
    
    def setCallback(self, callback):
        pass

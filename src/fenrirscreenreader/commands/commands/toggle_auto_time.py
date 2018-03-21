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
        return _('enables or disables automatic reading of time after an period')        
    
    def run(self):
        self.env['runtime']['settingsManager'].setSetting('time', 'enabled', str(not self.env['runtime']['settingsManager'].getSettingAsBool('time', 'enabled')))   
        if self.env['runtime']['settingsManager'].getSettingAsBool('time', 'enabled'): 
            self.env['runtime']['outputManager'].presentText(_("autotime enabled"), soundIcon='', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(_("autotime disabled"), soundIcon='', interrupt=True)                          
    
    def setCallback(self, callback):
        pass

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
        return _('enables or disables automatic reading of new text as it appears')        
    
    def run(self):
        self.env['runtime']['settingsManager'].setSetting('speech', 'autoReadIncoming', str(not self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'autoReadIncoming')))   
        if self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'autoReadIncoming'): 
            self.env['runtime']['outputManager'].presentText(_("autoread enabled"), soundIcon='', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(_("autoread disabled"), soundIcon='', interrupt=True)                          
    
    def setCallback(self, callback):
        pass

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
        return _('enables or disables announcement of emoticons instead of chars')        
    
    def run(self):
        self.env['runtime']['settingsManager'].setSetting('general', 'emoticons', str(not self.env['runtime']['settingsManager'].getSettingAsBool('general', 'emoticons')))   
        if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'emoticons'): 
            self.env['runtime']['outputManager'].presentText(_('emoticons enabled'), soundIcon='', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(_('emoticons disabled'), soundIcon='', interrupt=True)                          
    
    def setCallback(self, callback):
        pass

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
        return _('enables or disables the announcement of attributes')        
    
    def run(self):
        self.env['runtime']['settingsManager'].setSetting('general', 'hasAttributes', str(not self.env['runtime']['settingsManager'].getSettingAsBool('general', 'hasAttributes')))
        if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'hasAttributes'): 
            self.env['runtime']['outputManager'].presentText(_("announcement of attributes enabled"), soundIcon='', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(_("announcement of attributes disabled"), soundIcon='', interrupt=True)
    
    def setCallback(self, callback):
        pass

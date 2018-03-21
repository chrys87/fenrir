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
        return _('enables or disables tracking of highlighted text')        
    
    def run(self):
        currMode = self.env['runtime']['settingsManager'].getSettingAsBool('focus', 'highlight')

        self.env['runtime']['settingsManager'].setSetting('focus', 'highlight', str(not currMode))
        self.env['runtime']['settingsManager'].setSetting('focus', 'cursor', str(currMode))           
        if self.env['runtime']['settingsManager'].getSettingAsBool('focus', 'highlight'): 
            self.env['runtime']['outputManager'].presentText(_('highlight tracking'), soundIcon='', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(_('cursor tracking'), soundIcon='', interrupt=True)                          
    
    def setCallback(self, callback):
        pass

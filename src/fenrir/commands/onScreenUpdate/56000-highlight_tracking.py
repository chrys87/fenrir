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
        return _('enables or disables tracking of highlighted')        
    
    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('focus', 'highlight'):
            return
        self.env['runtime']['outputManager'].presentText(self.env['screen']['newAttribDelta'], soundIcon='', interrupt=True, flush=False)                          
    
    def setCallback(self, callback):
        pass

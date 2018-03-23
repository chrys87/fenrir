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
        return _('enables or disables automatic spell checking')            
    
    def run(self):      
        self.env['runtime']['settingsManager'].setSetting('general', 'autoSpellCheck', str(not self.env['runtime']['settingsManager'].getSettingAsBool('general', 'autoSpellCheck')))   
        if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'autoSpellCheck'): 
            self.env['runtime']['outputManager'].presentText(_("auto spellcheck enabled"), soundIcon='', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(_("auto spellcheck disabled"), soundIcon='', interrupt=True)                          
  
    def setCallback(self, callback):
        pass

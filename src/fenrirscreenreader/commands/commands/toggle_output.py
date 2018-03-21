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
        return _('toggles all output settings')        
    
    def run(self):
        if self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'enabled') or \
          self.env['runtime']['settingsManager'].getSettingAsBool('sound', 'enabled') or \
          self.env['runtime']['settingsManager'].getSettingAsBool('braille', 'enabled'):
            self.env['runtime']['outputManager'].presentText(_('Fenrir muted'), soundIcon='Accept', interrupt=True)          
            self.env['runtime']['settingsManager'].setSetting('speech', 'enabled','False')
            self.env['runtime']['settingsManager'].setSetting('sound', 'enabled','False')
            self.env['runtime']['settingsManager'].setSetting('braille', 'enabled','False')
        else:     
            self.env['runtime']['settingsManager'].setSetting('speech', 'enabled','True')
            self.env['runtime']['settingsManager'].setSetting('sound', 'enabled','True')
            self.env['runtime']['settingsManager'].setSetting('braille', 'enabled','True')
            self.env['runtime']['outputManager'].presentText(_('Fenrir unmuted'), soundIcon='Cancel', interrupt=True)                  

    def setCallback(self, callback):
        pass

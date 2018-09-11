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
        return _('Enables and disables Braille output')        

    def run(self):
        if self.env['runtime']['settingsManager'].getSettingAsBool('braille', 'enabled'): 
            self.env['runtime']['outputManager'].presentText(_('braille disabled'), soundIcon='BrailleOff', interrupt=True)
        self.env['runtime']['settingsManager'].setSetting('braille', 'enabled', str(not self.env['runtime']['settingsManager'].getSettingAsBool('braille', 'enabled')))   
        if self.env['runtime']['settingsManager'].getSettingAsBool('braille', 'enabled'): 
            self.env['runtime']['outputManager'].presentText(_('braille enabled'), soundIcon='BrailleOn', interrupt=True)                 

    def setCallback(self, callback):
        pass

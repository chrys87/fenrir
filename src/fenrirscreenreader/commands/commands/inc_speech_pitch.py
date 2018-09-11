#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import math

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('Increases the pitch of the speech')        
    
    def run(self):
        value = self.env['runtime']['settingsManager'].getSettingAsFloat('speech', 'pitch')
        value = round((math.ceil(10 * value) / 10) + 0.1, 2)
        if value > 1.0:
            value = 1.0  
        self.env['runtime']['settingsManager'].setSetting('speech', 'pitch', str(value))   

        self.env['runtime']['outputManager'].presentText(_("{0} percent speech pitch").format(int(value * 100)), soundIcon='', interrupt=True)
   
    def setCallback(self, callback):
        pass

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
        return _('adjusts the volume for in coming sounds')        

    def run(self):
        
        value = self.env['runtime']['settingsManager'].getSettingAsFloat('sound', 'volume')

        value = round((math.ceil(10 * value) / 10) + 0.1, 2)
        if value > 1.0:
            value = 1.0  
        self.env['runtime']['settingsManager'].setSetting('sound', 'volume', str(value))   

        self.env['runtime']['outputManager'].presentText(_("{0} percent sound volume").format(int(value * 100)),  soundIcon='SoundOn', interrupt=True)
 
    def setCallback(self, callback):
        pass

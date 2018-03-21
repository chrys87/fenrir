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
        return _('decrease sound volume')        

    def run(self):
        
        value = self.env['runtime']['settingsManager'].getSettingAsFloat('sound', 'volume')

        value = round((math.ceil(10 * value) / 10) - 0.1, 2)
        if value < 0.1:
            value = 0.1  
        self.env['runtime']['settingsManager'].setSetting('sound', 'volume', str(value))   

        self.env['runtime']['outputManager'].presentText(_("{0} percent sound volume").format(int(value * 100)), soundIcon='SoundOff', interrupt=True)
   
    def setCallback(self, callback):
        pass


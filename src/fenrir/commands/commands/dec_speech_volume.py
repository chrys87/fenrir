#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import math

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'decreases the volume of the speech'        
    
    def run(self):
        value = self.env['runtime']['settingsManager'].getSettingAsFloat('speech', 'volume')
        value = round((math.ceil(10 * value) / 10) - 0.1, 2)
        if value < 0.1:
            value = 0.1  
        self.env['runtime']['settingsManager'].setSetting('speech', 'volume', str(value))   

        self.env['runtime']['outputManager'].presentText(str(int(value * 100)) + " percent speech volume", soundIcon='', interrupt=True)

    def setCallback(self, callback):
        pass


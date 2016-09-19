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
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'increases the pitch of the speech'        
    
    def run(self, environment):
        value = environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'speech', 'pitch')
        value = round((math.ceil(10 * value) / 10) + 0.1, 2)
        if value > 1.0:
            value = 1.0  
        environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'pitch', str(value))   

        environment['runtime']['outputManager'].presentText(environment, str(int(value * 100)) + " percent speech pitch", soundIcon='', interrupt=True)
   
    def setCallback(self, callback):
        pass

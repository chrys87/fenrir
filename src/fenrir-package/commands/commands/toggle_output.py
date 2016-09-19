#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass 
    def getDescription(self, environment):
        return 'toggles all output settings'        
    
    def run(self, environment):
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled') or \
          environment['runtime']['settingsManager'].getSettingAsBool(environment, 'sound', 'enabled') or \
          environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled'):
            environment['runtime']['outputManager'].presentText(environment, "fenrir muted", soundIcon='Accept', interrupt=True)          
            environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'enabled','False')
            environment['runtime']['settingsManager'].setSetting(environment, 'sound', 'enabled','False')
            environment['runtime']['settingsManager'].setSetting(environment, 'braille', 'enabled','False')
        else:     
            environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'enabled','True')
            environment['runtime']['settingsManager'].setSetting(environment, 'sound', 'enabled','True')
            environment['runtime']['settingsManager'].setSetting(environment, 'braille', 'enabled','True')
            environment['runtime']['outputManager'].presentText(environment, "fenrir unmuted", soundIcon='Cancel', interrupt=True)                  

    def setCallback(self, callback):
        pass

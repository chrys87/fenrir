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
        return 'enables and disables output in braille'        

    def run(self, environment):
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "braille disabled", soundIcon='BrailleOff', interrupt=True)
        environment['runtime']['settingsManager'].setSetting(environment, 'braille', 'enabled', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "braille enabled", soundIcon='BrailleOn', interrupt=True)                 

    def setCallback(self, callback):
        pass

#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'No Description found'        
    def run(self, environment):
        
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "braille disabled", soundIcon='BrailleOff', interrupt=True)
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'braille', 'enabled', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "braille enabled", soundIcon='BrailleOn', interrupt=True)                 
        return environment    
    def setCallback(self, callback):
        pass

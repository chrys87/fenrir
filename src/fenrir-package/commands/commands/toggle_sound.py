#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'enables or disables sound'        
    def run(self, environment):
        
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'sound', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "sound disabled", soundIcon='SoundOff', interrupt=True)
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'sound', 'enabled', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'sound', 'enabled')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'sound', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "sound enabled", soundIcon='SoundOn', interrupt=True)                 
        return environment    
    def setCallback(self, callback):
        pass

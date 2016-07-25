#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'sound', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "sound disabled")
        else:
            environment['runtime']['outputManager'].presentText(environment, "sound enabled")
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'sound', 'enabled', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'sound', 'enabled')))            
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

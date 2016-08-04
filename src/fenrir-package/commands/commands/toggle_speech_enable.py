#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "speech disabled",soundIconName='SpeechOff', interrupt=True)
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'enabled', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "speech enabled",soundIconName='SpeechOn', interrupt=True)                 
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

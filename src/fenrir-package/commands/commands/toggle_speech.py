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
        
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "speech disabled", soundIcon='SpeechOff', interrupt=True)
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'enabled', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "speech enabled", soundIcon='SpeechOn', interrupt=True)                 
        return environment    
    def setCallback(self, callback):
        pass

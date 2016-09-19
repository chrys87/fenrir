#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass 
    def getDescription(self, environment):
        return 'enables or disables speech'        
    
    def run(self, environment):
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "speech disabled", soundIcon='SpeechOff', interrupt=True)
        environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'enabled', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "speech enabled", soundIcon='SpeechOn', interrupt=True)                 

    def setCallback(self, callback):
        pass

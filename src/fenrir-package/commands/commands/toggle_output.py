#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'toggles all output settings'        
    def run(self, environment):
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled') or \
          environment['runtime']['settingsManager'].getSettingAsBool(environment, 'sound', 'enabled') or \
          environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled'):
            environment['runtime']['outputManager'].presentText(environment, "fenrir muted", soundIcon='Accept', interrupt=True)          
            environment = environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'enabled','False')
            environment = environment['runtime']['settingsManager'].setSetting(environment, 'sound', 'enabled','False')
            environment = environment['runtime']['settingsManager'].setSetting(environment, 'braille', 'enabled','False')
        else:     
            environment = environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'enabled','True')
            environment = environment['runtime']['settingsManager'].setSetting(environment, 'sound', 'enabled','True')
            environment = environment['runtime']['settingsManager'].setSetting(environment, 'braille', 'enabled','True')
            environment['runtime']['outputManager'].presentText(environment, "fenrir unmuted", soundIcon='Cancel', interrupt=True)                  
        return environment    
    def setCallback(self, callback):
        pass

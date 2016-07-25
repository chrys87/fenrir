#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled'): 
            environment['runtime']['outputManager'].presentText(environment, "braille disabled")
        else:
            environment['runtime']['outputManager'].presentText(environment, "braille enabled")
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'braille', 'enabled', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled')))            
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

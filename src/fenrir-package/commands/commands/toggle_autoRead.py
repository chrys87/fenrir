#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'autoReadIncomming', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'autoReadIncomming')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'autoReadIncomming'): 
            environment['runtime']['outputManager'].presentText(environment, "autoread enabled", soundIconName='', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, "autoread disabled", soundIconName='', interrupt=True)                          
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

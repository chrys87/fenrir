#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'enables or disables automatic reading of new text as it appears'        
    def run(self, environment):
        
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'autoReadIncomming', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'autoReadIncomming')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'autoReadIncomming'): 
            environment['runtime']['outputManager'].presentText(environment, "autoread enabled", soundIcon='', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, "autoread disabled", soundIcon='', interrupt=True)                          
        return environment    
    def setCallback(self, callback):
        pass

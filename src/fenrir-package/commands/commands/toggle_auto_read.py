#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'enables or disables automatic reading of new text as it appears'        
    
    def run(self, environment):
        environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'autoReadIncomming', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'autoReadIncomming')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'autoReadIncomming'): 
            environment['runtime']['outputManager'].presentText(environment, "autoread enabled", soundIcon='', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, "autoread disabled", soundIcon='', interrupt=True)                          
    
    def setCallback(self, callback):
        pass

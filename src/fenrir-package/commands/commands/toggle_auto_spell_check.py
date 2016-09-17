#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return 'enables or disables automatic spell checking'            
    
    def run(self, environment):      
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'general', 'autoSpellCheck', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'general', 'autoSpellCheck')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'general', 'autoSpellCheck'): 
            environment['runtime']['outputManager'].presentText(environment, "auto spellcheck enabled", soundIcon='', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, "auto spellcheck disabled", soundIcon='', interrupt=True)                          
        return environment    
    def setCallback(self, callback):
        pass

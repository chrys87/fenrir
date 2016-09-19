#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'enables or disables automatic spell checking'            
    
    def run(self, environment):      
        environment['runtime']['settingsManager'].setSetting(environment, 'general', 'autoSpellCheck', str(not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'general', 'autoSpellCheck')))   
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'general', 'autoSpellCheck'): 
            environment['runtime']['outputManager'].presentText(environment, "auto spellcheck enabled", soundIcon='', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, "auto spellcheck disabled", soundIcon='', interrupt=True)                          
  
    def setCallback(self, callback):
        pass

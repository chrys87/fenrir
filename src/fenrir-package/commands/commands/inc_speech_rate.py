#!/bin/python
import math

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return 'increase the speech rat'        
    
    def run(self, environment):
        value = environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'speech', 'rate')
        value = round((math.ceil(10 * value) / 10) + 0.1, 2)
        if value > 1.0:
            value = 1.0  
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'rate', str(value))   

        environment['runtime']['outputManager'].presentText(environment, str(int(value * 100)) + " percent speech rate", soundIcon='', interrupt=True)
               
        return environment    
    def setCallback(self, callback):
        pass

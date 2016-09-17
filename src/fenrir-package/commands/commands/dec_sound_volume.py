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
        return 'decrease sound volume'        

    def run(self, environment):
        
        value = environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'sound', 'volume')

        value = round((math.ceil(10 * value) / 10) - 0.1, 2)
        if value < 0.1:
            value = 0.1  
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'sound', 'volume', str(value))   

        environment['runtime']['outputManager'].presentText(environment, str(int(value * 100)) + " percent sound volume", soundIcon='SoundOff', interrupt=True)
               
        return environment    
    def setCallback(self, callback):
        pass


#!/bin/python
import math

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'adjusts the volume for in coming sounds'        

    def run(self, environment):
        
        value = environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'sound', 'volume')

        value = round((math.ceil(10 * value) / 10) + 0.1, 2)
        if value > 1.0:
            value = 1.0  
        environment['runtime']['settingsManager'].setSetting(environment, 'sound', 'volume', str(value))   

        environment['runtime']['outputManager'].presentText(environment, str(int(value * 100)) + " percent sound volume", soundIcon='SoundOn', interrupt=True)
 
    def setCallback(self, callback):
        pass

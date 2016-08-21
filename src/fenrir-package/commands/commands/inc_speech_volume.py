#!/bin/python
import math

class command():
    def __init__(self):
        pass
    def run(self, environment):
        
        value = environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'speech', 'volume')

        value = round((math.ceil(10 * value) / 10) + 0.1, 2)
        if value > 1.0:
            value = 1.0  
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'volume', str(value))   

        environment['runtime']['outputManager'].presentText(environment, str(int(value * 100)) + " percent speech volume", soundIcon='SpeechOn', interrupt=True)
               
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

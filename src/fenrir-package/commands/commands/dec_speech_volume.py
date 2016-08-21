#!/bin/python
import math

class command():
    def __init__(self):
        pass
    def run(self, environment):
        
        value = environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'speech', 'volume')

        value = round((math.ceil(20 * value) / 20) - 0.1, 2)
        if value < 0.1:
            value = 0.1  
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'volume', str(value))   

        environment['runtime']['outputManager'].presentText(environment, str(int(value * 100)) + " percent speech volume", soundIcon='SpeechOff', interrupt=True)
               
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

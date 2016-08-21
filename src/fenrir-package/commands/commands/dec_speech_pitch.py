#!/bin/python
import math

class command():
    def __init__(self):
        pass
    def run(self, environment):
        
        value = environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'speech', 'pitch')

        value = round((math.ceil(20 * value) / 20) - 0.1, 2)
        if value < 0.0:
            value = 0.0 
        environment = environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'pitch', str(value))   

        environment['runtime']['outputManager'].presentText(environment, str(int(value * 100)) + " percent speech pitch", soundIcon='SpeechOff', interrupt=True)
               
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

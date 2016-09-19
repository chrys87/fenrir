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
        return 'decreases the pitch of the speech'        
    
    def run(self, environment):
        value = environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'speech', 'pitch')
        value = round((math.ceil(10 * value) / 10) - 0.1, 2)
        if value < 0.0:
            value = 0.0 
        environment['runtime']['settingsManager'].setSetting(environment, 'speech', 'pitch', str(value))   

        environment['runtime']['outputManager'].presentText(environment, str(int(value * 100)) + " percent speech pitch", soundIcon='', interrupt=True)
 
    def setCallback(self, callback):
        pass

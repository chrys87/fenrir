#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return ''        
    def run(self, environment):
 
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'charDeleteEcho'):
            return environment
   
        # detect typing or chilling
        if environment['screenData']['newCursor']['x'] >= environment['screenData']['oldCursor']['x']:
            return environment 

        # TTY change
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return environment

        # More than just a deletion happend
        if environment['screenData']['newDelta'].strip() != '':
            if environment['screenData']['newDelta'] != environment['screenData']['oldDelta']:
    	        return environment
            
        # No deletion 
        if environment['screenData']['newNegativeDelta'] == '':
            return environment

        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newNegativeDelta'], interrupt=True)
        return environment
    def setCallback(self, callback):
        pass


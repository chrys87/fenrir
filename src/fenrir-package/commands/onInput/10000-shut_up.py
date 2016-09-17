#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self, environment):
        return ''               
    
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'interruptOnKeyPress'):
            return environment     
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return environment              
#        if environment['screenData']['newCursor'] == environment['screenData']['oldCursor'] and\
#          environment['screenData']['newDelta'] == environment['screenData']['oldDelta']:
#            return environment
        if environment['input']['currShortcut'] != '':
            return environment
        environment['runtime']['outputManager'].interruptOutput(environment)
        return environment
    def setCallback(self, callback):
        pass

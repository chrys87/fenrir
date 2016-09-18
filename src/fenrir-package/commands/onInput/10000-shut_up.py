#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return ''               
    
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'interruptOnKeyPress'):
            return 
        if environment['runtime']['inputManager'].noKeyPressed(environment):
            return
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return               
#        if environment['screenData']['newCursor'] == environment['screenData']['oldCursor'] and\
#          environment['screenData']['newDelta'] == environment['screenData']['oldDelta']:
#            return environment
        environment['runtime']['outputManager'].interruptOutput(environment)

    def setCallback(self, callback):
        pass

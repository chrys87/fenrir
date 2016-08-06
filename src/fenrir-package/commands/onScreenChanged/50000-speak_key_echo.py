#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
 
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'charEcho'):
            return environment 
        if environment['screenData']['newCursor']['x'] <= environment['screenData']['oldCursor']['x']:
            return environment 

        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return environment

        if environment['screenData']['newDelta'] == environment['screenData']['oldDelta']:
            return environment
             
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=True)

        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

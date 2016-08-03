#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'charEcho') and\
          environment['screenData']['newCursor']['x'] - environment['screenData']['oldCursor']['x'] ==1:
            return environment 

        ttyChanged = environment['screenData']['newTTY'] != environment['screenData']['oldTTY']
        if environment['screenData']['newDelta'] == environment['screenData']['oldDelta'] and \
          not ttyChanged:
            return environment
            
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], soundIconName='', interrupt=ttyChanged)
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

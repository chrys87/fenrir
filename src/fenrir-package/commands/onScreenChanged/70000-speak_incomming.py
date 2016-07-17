#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'charEcho') and\
          len(environment['screenData']['newDelta']) <= 2 and \
          environment['screenData']['newCursor'] != environment['screenData']['oldCursor']:
            return environment 
        if environment['screenData']['newDelta'] == environment['screenData']['oldDelta'] and \
          environment['screenData']['newTTY'] == environment['screenData']['oldTTY']:
            return environment
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'],False)
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

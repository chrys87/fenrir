#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'autoReadIncomming'):
            return environment

        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return environment
        if environment['screenData']['newDelta'] == '':
            return environment
           
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=False)

        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

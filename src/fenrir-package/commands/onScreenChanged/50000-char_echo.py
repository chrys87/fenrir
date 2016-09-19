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
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'charEcho'):
            return
        # detect deletion or chilling 
        if environment['screenData']['newCursor']['x'] <= environment['screenData']['oldCursor']['x']:
            return 
        # TTY Change
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return
        # is there any change?
        if environment['screenData']['newDelta'] == '':
            return
        # big changes are no char (but the value is bigger than one maybe the differ needs longer than you can type, so a little strange random buffer for now)
        if len(environment['screenData']['newDelta']) > 3:
            return        
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=True)

    def setCallback(self, callback):
        pass


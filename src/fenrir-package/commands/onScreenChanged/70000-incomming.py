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
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'autoReadIncomming'):
            return environment
        # is there something to read?
        if environment['screenData']['newDelta'] == '':
            return environment            
        # dont read TTY change
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return environment
        # its a cursor movement (experimental) - maybe also check current shortcut string?
        if abs(environment['screenData']['newCursor']['x'] - environment['screenData']['oldCursor']['x']) >= 1:
            if len(environment['screenData']['newDelta']) <= 5:
                return environment          
    
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=False)

        return environment
    def setCallback(self, callback):
        pass


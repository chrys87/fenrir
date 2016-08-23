#!/bin/python
import time

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'promote', 'enabled'):
            return environment
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return environment
        if environment['screenData']['newDelta'] == '':
            return environment
        if int(time.time() - environment['input']['lastInputTime']) < environment['runtime']['settingsManager'].getSettingAsInt(environment, 'promote', 'inactiveTimeoutSec'):
            return environment
        if len(environment['runtime']['settingsManager'].getSetting(environment, 'promote', 'list')) == 0:
            return environment       
        for promote in environment['runtime']['settingsManager'].getSetting(environment, 'promote', 'list').split(','):
            if promote in environment['screenData']['newDelta']:    
                environment['runtime']['outputManager'].playSoundIcon(environment,'PromotedText')        
                environment['input']['lastInputTime'] = time.time()
                return environment

        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

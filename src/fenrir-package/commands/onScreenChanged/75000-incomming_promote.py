#!/bin/python
import time

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
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'promote', 'enabled'):
            return
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return
        if environment['screenData']['newDelta'] == '':
            return
        if int(time.time() - environment['input']['lastInputTime']) < environment['runtime']['settingsManager'].getSettingAsInt(environment, 'promote', 'inactiveTimeoutSec'):
            return
        if len(environment['runtime']['settingsManager'].getSetting(environment, 'promote', 'list')) == 0:
            return       
        for promote in environment['runtime']['settingsManager'].getSetting(environment, 'promote', 'list').split(','):
            if promote in environment['screenData']['newDelta']:    
                environment['runtime']['outputManager'].playSoundIcon(environment,'PromotedText')        
                environment['input']['lastInputTime'] = time.time()
                return

    def setCallback(self, callback):
        pass


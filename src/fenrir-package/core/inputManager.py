#!/bin/python

import time
from utils import debug

class inputManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        environment['runtime']['settingsManager'].loadDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'keyboard', 'driver'), 'inputDriver')     

    def shutdown(self, environment):
        environment['runtime']['inputManager'].releaseDevices(environment)    
        if environment['runtime']['inputDriver']:
            environment['runtime']['inputDriver'].shutdown(environment)
    
    def proceedInputEvent(self, environment):
        timeout = True    	
        event = environment['runtime']['inputDriver'].getInput(environment)
        if event:
            timeout = False
            environment['input']['firstEvent'] = event
            environment['input']['currEvent'] = event
            #if not 
            #print(event)
       
        return timeout
    
    def grabDevices(self, environment):
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'grabDevices'):
            environment['runtime']['inputDriver'].grabDevices(environment)

    def releaseDevices(self, environment):
        environment['runtime']['inputDriver'].releaseDevices()
        
    def isConsumeInput(self, environment):
	    return environment['input']['consumeKey'] and \
          not environment['input']['keyForeward'] or \
          not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'grabDevices')
          
    def passInput(self, environment):
        try:
            environment['runtime']['inputDriver']
        except Exception as e:
            environment['runtime']['debug'].writeDebugOut(environment,"Error while writeUInput",debug.debugLevel.ERROR)
            environment['runtime']['debug'].writeDebugOut(environment, str(e),debug.debugLevel.ERROR)    
        return environment

    def getPrevDeepestInput(self, environment):
        shortcut = []
        shortcut.append(environment['input']['shortcutRepeat'])
        shortcut.append(sorted(environment['input']['prevDeepestInput']))

    def getPrevShortcut(self, environment):
        shortcut = []
        shortcut.append(environment['input']['shortcutRepeat'])
        shortcut.append(sorted(environment['input']['prevInput']))

    def getPrevShortcut(self, environment):
        shortcut = []
        shortcut.append(environment['input']['shortcutRepeat'])
        shortcut.append(sorted(environment['input']['prevInput']))
        
    def isFenrirKey(self,environment, event):
        return str(event.code) in environment['input']['fenrirKey']

    def getCommandForShortcut(self, environment, shortcut):
        shortcut = shortcut.upper()
        if not self.shortcutExists(environment, shortcut):
            return '' 
        return environment['bindings'][shortcut].upper()

    def shortcutExists(self, environment, shortcut):
        return( str(shortcut).upper() in environment['bindings'])
        

#!/bin/python

import time
from utils import debug

class inputManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment
    def proceedInputEvent(self, environment):
        timeout = True    	
        event = environment['runtime']['inputDriver'].getInput(environment)
        if event:
            timeout = False
            print(event)
        return environment, timeout
    
    def grabDevices(self, environment):
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

    def getShortcutString(self, environment):
        if environment['input']['currShortcut'] == {}:
            return '' 
        currShortcutStringList = []
        for key in environment['input']['currShortcut']:
             currShortcutStringList.append("%s-%s" % (environment['input']['currShortcut'][key], key))
        currShortcutStringList = sorted(currShortcutStringList)
        return str(currShortcutStringList)[1:-1].replace(" ","").replace("'","")
        
    def isFenrirKey(self,environment, event):
        return str(event.code) in environment['input']['fenrirKey']        

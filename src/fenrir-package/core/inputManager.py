#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from core import debug
from core import inputEvent

class inputManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        environment['runtime']['settingsManager'].loadDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'keyboard', 'driver'), 'inputDriver')     
        # init LEDs with current state
        environment['input']['newNumLock'] = environment['runtime']['inputDriver'].getNumlock(environment) 
        environment['input']['oldNumLock'] = environment['input']['newNumLock']
        environment['input']['newCapsLock'] = environment['runtime']['inputDriver'].getCapslock(environment)       
        environment['input']['oldCapsLock'] = environment['input']['newCapsLock']         
        environment['input']['newScrollLock'] = environment['runtime']['inputDriver'].getScrollLock(environment)            
        environment['input']['oldScrollLock'] = environment['input']['newScrollLock']         
        self.grabDevices(environment)

    def shutdown(self, environment):
        environment['runtime']['inputManager'].releaseDevices(environment)    
        if environment['runtime']['inputDriver']:
            environment['runtime']['inputDriver'].shutdown(environment)
            del environment['runtime']['inputDriver']
    
    def getInputEvent(self, environment):
        eventReceived = False    	
        mEvent = environment['runtime']['inputDriver'].getInput(environment)
        mEvent['EventName'] = self.convertEventName(mEvent['EventName'])
        if mEvent:
            if mEvent['EventValue'] == 0:
                return False  
            eventReceived = True
            if mEvent['EventState'] == 0:
                if mEvent['EventName'] in environment['input']['currInput']:
                    environment['input']['currInput'].remove(mEvent['EventName'])
                    environment['input']['currInput'] = sorted(environment['input']['currInput'])                    
            elif mEvent['EventState'] == 1:
    	        if not mEvent['EventName'] in environment['input']['currInput']:                                
    	            environment['input']['currInput'].append(mEvent['EventName'])            
                    environment['input']['currInput'] = sorted(environment['input']['currInput'])
            elif mEvent['EventState'] == 2:
                pass
            else:
                pass  
            environment['input']['oldNumLock'] = environment['input']['newNumLock']
            environment['input']['newNumLock'] = environment['runtime']['inputDriver'].getNumlock(environment) 
            environment['input']['oldCapsLock'] = environment['input']['newCapsLock'] 
            environment['input']['newCapsLock'] = environment['runtime']['inputDriver'].getCapslock(environment)       
            environment['input']['oldScrollLock'] = environment['input']['newScrollLock'] 
            environment['input']['newScrollLock'] = environment['runtime']['inputDriver'].getScrollLock(environment)                     
            environment['input']['lastInputTime'] = time.time()
            environment['input']['shortcutRepeat'] = 1
        return eventReceived
    
    def grabDevices(self, environment):
        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'grabDevices'):
            environment['runtime']['inputDriver'].grabDevices(environment)

    def releaseDevices(self, environment):
        environment['runtime']['inputDriver'].releaseDevices(environment)

    def convertEventName(self,  eventName):
        if eventName == 'KEY_LEFTCTRL':
            eventName == 'KEY_CTRL'
        elif eventName == 'KEY_RIGHTCTRL':
            eventName = 'KEY_CTRL'
        elif eventName == 'KEY_LEFTSHIFT':
            eventName = 'KEY_SHIFT'
        elif eventName == 'KEY_RIGHTSHIFT':
            eventName = 'KEY_SHIFT'
        elif eventName == 'KEY_LEFTALT':
            eventName = 'KEY_ALT'
        elif eventName == 'KEY_RIGHTALT':
            eventName = 'KEY_ALT'
        if self.isFenrirKey(environment, eventName):
            eventName = 'KEY_FENRIR'    	
    	return eventName
    	
    def isConsumeInput(self, environment):
	    return environment['runtime']['commandManager'].isCommandQueued(environment) and \
	      not environment['input']['keyForeward']
	    #and
	    #  not (environment['input']['keyForeward'] or \
        #  environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'grabDevices'))
 
    def clearEventBuffer(self, environment):
        environment['runtime']['inputDriver'].clearEventBuffer(environment) 
          
    def writeEventBuffer(self, environment):
        try:
            environment['runtime']['inputDriver'].writeEventBuffer(environment)
        except Exception as e:
            print(e)
            environment['runtime']['debug'].writeDebugOut(environment,"Error while writeUInput",debug.debugLevel.ERROR)
            environment['runtime']['debug'].writeDebugOut(environment, str(e),debug.debugLevel.ERROR)    
    def isFenrirKeyPressed(self, environment):
        return 'KEY_FENRIR' in environment['input']['currInput']

    def noKeyPressed(self, environment):
        return environment['input']['currInput'] == []
    def getPrevDeepestInput(self, environment):
        shortcut = []
        shortcut.append(environment['input']['shortcutRepeat'])
        shortcut.append(sorted(environment['input']['prevDeepestInput']))

    def getPrevShortcut(self, environment):
        shortcut = []
        shortcut.append(environment['input']['shortcutRepeat'])
        shortcut.append(sorted(environment['input']['prevInput']))
        return str(shortcut)

    def getCurrShortcut(self, environment):
        shortcut = []
        shortcut.append(environment['input']['shortcutRepeat'])
        shortcut.append(sorted(environment['input']['currInput']))
        return str(shortcut)
        
    def isFenrirKey(self,environment, eventName):
        return eventName in environment['input']['fenrirKey']

    def getCommandForShortcut(self, environment, shortcut):
        shortcut = shortcut.upper()
        if not self.shortcutExists(environment, shortcut):
            return '' 
        return environment['bindings'][shortcut].upper()

    def shortcutExists(self, environment, shortcut):
        return( str(shortcut).upper() in environment['bindings'])
        

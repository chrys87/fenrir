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
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('keyboard', 'driver'), 'inputDriver')
        # init LEDs with current state
        self.env['input']['newNumLock'] = self.env['runtime']['inputDriver'].getNumlock()
        self.env['input']['oldNumLock'] = self.env['input']['newNumLock']
        self.env['input']['newCapsLock'] = self.env['runtime']['inputDriver'].getCapslock()
        self.env['input']['oldCapsLock'] = self.env['input']['newCapsLock']
        self.env['input']['newScrollLock'] = self.env['runtime']['inputDriver'].getScrollLock()
        self.env['input']['oldScrollLock'] = self.env['input']['newScrollLock']
        self.grabDevices()

    def shutdown(self):
        self.env['runtime']['inputManager'].releaseDevices()
        self.env['runtime']['settingsManager'].shutdownDriver('inputDriver')

    def getInputEvent(self):
        eventReceived = False
        mEvent = self.env['runtime']['inputDriver'].getInputEvent()
        if mEvent:
            mEvent['EventName'] = self.convertEventName(mEvent['EventName'])        
            eventReceived = True
            if mEvent['EventState'] == 0:
                if mEvent['EventName'] in self.env['input']['currInput']:
                    self.env['input']['currInput'].remove(mEvent['EventName'])
                    if len(self.env['input']['currInput']) > 1:
                        self.env['input']['currInput'] = sorted(self.env['input']['currInput'])
                    if len(self.env['input']['currInput']) == 0:
                        self.env['input']['prevDeepestInput'] = []
                        self.env['input']['shortcutRepeat'] = 1 
                    self.env['input']['lastInputTime'] = time.time()                                                   
            elif mEvent['EventState'] == 1:
                if not mEvent['EventName'] in self.env['input']['currInput']:
                    self.env['input']['currInput'].append(mEvent['EventName'])
                    if len(self.env['input']['currInput']) > 1:
                        self.env['input']['currInput'] = sorted(self.env['input']['currInput'])
                    if len(self.env['input']['prevDeepestInput']) < len(self.env['input']['currInput']):
                        self.env['input']['prevDeepestInput'] = self.env['input']['currInput'].copy()
                    elif self.env['input']['prevDeepestInput'] == self.env['input']['currInput']:
                        if time.time() - self.env['input']['lastInputTime']  <= self.env['runtime']['settingsManager'].getSettingAsFloat('keyboard','doubleTapDelay'):
                            self.env['input']['shortcutRepeat'] += 1
                        else:
                            self.env['input']['shortcutRepeat'] = 1
                    self.env['input']['lastInputTime'] = time.time()                                               
            elif mEvent['EventState'] == 2:
                pass
            else:
                pass  
            self.env['input']['oldNumLock'] = self.env['input']['newNumLock']
            self.env['input']['newNumLock'] = self.env['runtime']['inputDriver'].getNumlock()
            self.env['input']['oldCapsLock'] = self.env['input']['newCapsLock'] 
            self.env['input']['newCapsLock'] = self.env['runtime']['inputDriver'].getCapslock()
            self.env['input']['oldScrollLock'] = self.env['input']['newScrollLock'] 
            self.env['input']['newScrollLock'] = self.env['runtime']['inputDriver'].getScrollLock()

        return eventReceived
    
    def grabDevices(self):
        if self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'grabDevices'):
            self.env['runtime']['inputDriver'].grabDevices()

    def releaseDevices(self):
        try:
            self.env['runtime']['inputDriver'].releaseDevices()
        except:
            pass

    def convertEventName(self, eventName):
        if not eventName:
            return ''
        if eventName == '':
            return ''
        eventName = eventName.upper()
        if eventName == 'KEY_LEFTCTRL':
            eventName = 'KEY_CTRL'         
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
        elif eventName == 'KEY_LEFTMETA':
            eventName = 'KEY_META'
        elif eventName == 'KEY_RIGHTMETA':
            eventName = 'KEY_META'            
        if self.isFenrirKey(eventName):
            eventName = 'KEY_FENRIR'
        return eventName
	
    def isConsumeInput(self):
        return self.env['runtime']['commandManager'].isCommandQueued() and \
          not self.env['input']['keyForeward']
        #and
        #  not (self.env['input']['keyForeward'] or \
        #  self.env['runtime']['settingsManager'].getSettingAsBool(, 'keyboard', 'grabDevices'))
 
    def clearEventBuffer(self):
        self.env['runtime']['inputDriver'].clearEventBuffer()
          
    def writeEventBuffer(self):
        try:
            if self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'grabDevices'):
                self.env['runtime']['inputDriver'].writeEventBuffer()
                time.sleep(0.008)
            self.clearEventBuffer()
            if len(self.env['input']['currInput']) == 1:              
                if self.env['input']['currInput'][0] in ['KEY_UP','KEY_DOWN']:              
                    time.sleep(0.08) # hack for tintin history because it needs more time
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("Error while writeUInput",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)

    def isFenrirKeyPressed(self):
        return 'KEY_FENRIR' in self.env['input']['currInput']

    def noKeyPressed(self):
        return self.env['input']['currInput'] == []
        
    def getPrevDeepestInput(self):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        shortcut.append(self.env['input']['prevDeepestInput'])

    def getPrevShortcut(self):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        shortcut.append(self.env['input']['prevInput'])
        return str(shortcut)

    def getCurrShortcut(self):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        shortcut.append(self.env['input']['currInput'])
        return str(shortcut)
        
    def isFenrirKey(self, eventName):
        return eventName in self.env['input']['fenrirKey']

    def getCommandForShortcut(self, shortcut):
        if not self.shortcutExists(shortcut):
            return '' 
        return self.env['bindings'][shortcut]

    def shortcutExists(self, shortcut):
        return(shortcut in self.env['bindings'])

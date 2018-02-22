#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from core import debug

class inputManager():
    def __init__(self):
        self.setLedState = True
        self.currInput = []
        self.prevDeepestInput = []
        self.eventBuffer = []
        self.shortcutRepeat = 0
        self.fenrirKey = []
        self.scriptKey = []
        self.keyForeward = 0
        self.lastInputTime = time.time()
        self.lastDeepestInput = []
        self.NumLock = {'prev': True, 'current': True }
        self.ScrollLock = {'prev': True, 'current': True }
        self.CapsLock = {'prev': False, 'current': False }
    def setCurrInput(self, value):
        if len(self.getCurrInput()) > 1:
            self.currInput = sorted(self.getCurrInput())  
    def getCurrInput(self):
        return self.currInput
    def addToCurrInput(self, value):
        currInput = self.getCurrInput().append(value)
        if len(currInput) > 1:
            currInput = sorted(currInput)                
        self.setCurrInput(currInput)
    def removeFromCurrInput(self, value):        
        currInput = self.getCurrInput().remove(value)
        if len(currInput) > 1:
            currInput = sorted(currInput)        
        self.setCurrInput(currInput)
    def increaseShortcutRepeat(self):
        self.shortcutRepeat += 1    
    def resetShortcutRepeat(self):
        self.shortcutRepeat = 1
    def getShortcutRepeat(self):
        return self.shortcutRepeat
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('keyboard', 'driver'), 'inputDriver')
        self.updateInputDevices()
        # init LEDs with current state
        self.setNumLock(self.env['runtime']['inputDriver'].getLedState())
        self.setNumLock(self.getNumLock())
        self.setCapsLock(self.env['runtime']['inputDriver'].getLedState(1))
        self.setCapsLock(self.getCapsLock())
        self.setScrollLock(self.env['runtime']['inputDriver'].getLedState(2))
        self.setScrollLock(self.getScrollLock())
    def shutdown(self):
        self.removeAllDevices()
        self.env['runtime']['settingsManager'].shutdownDriver('inputDriver')
    def newMappedInputEvent(self):
        return {
        'EventName': '',
        'EventValue': '',
        'EventSec': 0,
        'EventUsec': 0,
        'EventState': 0,
        }    
    def getInputEvent(self):
        return self.env['runtime']['inputDriver'].getInputEvent()
    def handleInputEvent(self, mEvent = None):
        eventReceived = False
        if mEvent:
            mEvent['EventName'] = self.convertEventName(mEvent['EventName'])        
            eventReceived = True
            self.prevInput = self.getCurrInput().copy()
            if mEvent['EventState'] == 0:
                if mEvent['EventName'] in self.getCurrInput():
                    self.removeFromCurrInput(mEvent['EventName'])
                    elif len(self.getCurrInput()) == 0:
                        self.env['input']['shortcutRepeat'] = 1 
                    self.setLedState = self.handleLedStates(mEvent)                                             
                    self.lastInputTime = time.time()                                                   
            elif mEvent['EventState'] == 1:
                if not mEvent['EventName'] in self.getCurrInput():
                    self.addToCurrInput(mEvent['EventName'])
                    if len(self.lastDeepestInput) < len(self.getCurrInput()):
                        self.setLastDeepestInput( self.getCurrInput().copy())
                    elif self.lastDeepestInput == self.getCurrInput():
                        if time.time() - self.lastInputTime <= self.env['runtime']['settingsManager'].getSettingAsFloat('keyboard','doubleTapTimeout'):
                            self.increaseShortcutRepeat()
                        else:
                            self.resetShortcutRepeat()
                    self.setLedState = self.handleLedStates(mEvent)                                             
                    self.lastInputTime = time.time()                                               
            elif mEvent['EventState'] == 2:
                self.lastInputTime  = time.time()                                                   
            else:
                pass  
            self.setScrollLock(self.env['runtime']['inputDriver'].getLedState(2))
            self.setNumLock(self.env['runtime']['inputDriver'].getLedState())
            self.setCapsLock(self.env['runtime']['inputDriver'].getLedState(1))
            self.env['runtime']['debug'].writeDebugOut("currInput " + str(self.getCurrInput() ) ,debug.debugLevel.INFO)              
            if self.noKeyPressed():
                self.prevInput = []
                self.setLedState = True
        return eventReceived

    def handleLedStates(self, mEvent):
        if not self.setLedState:
            return self.setLedState
        if mEvent['EventName'] == 'KEY_NUMLOCK':
            if mEvent['EventState'] == 1 and not self.getNumLock() == 1:
                self.env['runtime']['inputDriver'].toggleLedState() 
                return False
            if mEvent['EventState'] == 0 and not self.getNumLock() == 0:
                self.env['runtime']['inputDriver'].toggleLedState()                                                                        
                return False
        if mEvent['EventName'] == 'KEY_CAPSLOCK':   
            if mEvent['EventState'] == 1 and not self.getCapsLock() == 1:
                self.env['runtime']['inputDriver'].toggleLedState(1)              
                return False
            if mEvent['EventState'] == 0 and not self.getCapsLock() == 0:
                self.env['runtime']['inputDriver'].toggleLedState(1)                                                                         
                return False                                      
        if mEvent['EventName'] == 'KEY_SCROLLLOCK':  
            if mEvent['EventState'] == 1 and not self.getScrollLock() == 1:
                self.env['runtime']['inputDriver'].toggleLedState(2)              
                return False
            if mEvent['EventState'] == 0 and not self.getScrollLock() == 0:
                self.env['runtime']['inputDriver'].toggleLedState(2)                                                                       
                return False
        return self.setLedState

    def grabAllDevices(self):
        if self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'grabDevices'):
            self.env['runtime']['inputDriver'].grabAllDevices()
    
    def updateInputDevices(self):
        try:
            self.env['runtime']['inputDriver'].updateInputDevices()  
        except:
            pass
    
    def removeAllDevices(self):
        try:
            self.env['runtime']['inputDriver'].removeAllDevices()
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
        if self.isScriptKey(eventName):
            eventName = 'KEY_SCRIPT'            
        return eventName

    def clearEventBuffer(self):
        self.env['runtime']['inputDriver'].clearEventBuffer()
    def setLastDeepestInput(self, currentDeepestInput):
        self.lastDeepestInput = currentDeepestInput
    def clearLastDeepInput(self):
        self.lastDeepestInput = []  
    def getLastInputTime(self):
        return self.lastInputTime           
    def getLastDeepestInput(self):
        return self.lastDeepestInput 
    def writeEventBuffer(self):
        try:
            if self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'grabDevices'):
                self.env['runtime']['inputDriver'].writeEventBuffer()
            self.clearEventBuffer()
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("Error while writeUInput",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)

    def noKeyPressed(self):
        return self.env['input']['currInput'] == []
    def isKeyPress(self):
        return (self.env['input']['prevInput'] == []) and (self.env['input']['currInput'] != [])
    def getPrevDeepestShortcut(self):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        shortcut.append(self.getLastDeepestInput())
        return str(shortcut)
        
    def getPrevShortcut(self):
        shortcut = []
        shortcut.append(self.env['input']['shortcutRepeat'])
        shortcut.append(self.env['input']['prevInput'])
        return str(shortcut)

    def getCurrShortcut(self, inputSequence = None):
        shortcut = []
        shortcut.append(self.getShortcutRepeat())
        if inputSequence:
            shortcut.append(inputSequence)
        else:        
            shortcut.append(self.getCurrInput())
        if len(self.env['input']['prevInput']) < len(self.getCurrInput()):
            if self.getShortcutRepeat() > 1  and not self.shortcutExists(str(shortcut)):
                shortcut = []
                self.resetShortcutRepeat()
                shortcut.append(self.env['input']['shortcutRepeat'])
                shortcut.append(self.getCurrInput())     
        self.env['runtime']['debug'].writeDebugOut("currShortcut " + str(shortcut) ,debug.debugLevel.INFO)                      
        return str(shortcut)
        
    def currKeyIsModifier(self):
        if len(self.getLastDeepestInput()) != 1:
            return False
        return (self.getCurrInput()[0] =='KEY_FENRIR') or (self.getCurrInput()[0] == 'KEY_SCRIPT')
    
    def isFenrirKey(self, eventName):
        return eventName in self.env['input']['fenrirKey']
    
    def isScriptKey(self, eventName):
        return eventName in self.env['input']['scriptKey']
    
    def getCommandForShortcut(self, shortcut):
        if not self.shortcutExists(shortcut):
            return '' 
        return self.env['bindings'][shortcut]

    def shortcutExists(self, shortcut):
        return(shortcut in self.env['bindings'])
    def setNumLock(self, value):
        self.NumLock['prev'] = self.NumLock['current']
        self.NumLock['current'] = value
    def setScrollLock(self, value):
        self.ScrollLock['prev'] = self.ScrollLock['current']
        self.ScrollLock['current'] = value
    def setCapsLock(self, value):
        self.CapsLock['prev'] = self.CapsLock['current']
        self.CapsLock['current'] = value

    def getNumLock(self, what = 'current'):
        return self.NumLock[what]
    def getScrollLock(self, what = 'current'):
        return self.ScrollLock[what]
    def getCapsLock(self, what = 'current'):
        return self.CapsLock[what]        

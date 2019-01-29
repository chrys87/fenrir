#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core import inputData
import os, inspect, time
currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
fenrirPath = os.path.dirname(currentdir)

class inputManager():
    def __init__(self):
        self.shortcutType = 'KEY'
        self.executeDeviceGrab = False        
    def setShortcutType(self, shortcutType = 'KEY'):
        if shortcutType in ['KEY', 'BYTE']:
            self.shortcutType = shortcutType
    def getShortcutType(self):
        return self.shortcutType
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('keyboard', 'driver'), 'inputDriver')
        self.updateInputDevices()

        # init LEDs with current state
        self.env['input']['newNumLock'] = self.env['runtime']['inputDriver'].getLedState()
        self.env['input']['oldNumLock'] = self.env['input']['newNumLock']
        self.env['input']['newCapsLock'] = self.env['runtime']['inputDriver'].getLedState(1)
        self.env['input']['oldCapsLock'] = self.env['input']['newCapsLock']
        self.env['input']['newScrollLock'] = self.env['runtime']['inputDriver'].getLedState(2)
        self.env['input']['oldScrollLock'] = self.env['input']['newScrollLock']
        self.lastDeepestInput = []
        self.env['input']['shortcutRepeat'] = 1
        self.lastInputTime = time.time()
    def shutdown(self):
        self.removeAllDevices()
        self.env['runtime']['settingsManager'].shutdownDriver('inputDriver')
    def  getInputEvent(self):
        event =  None
        try:
            event = self.env['runtime']['inputDriver'].getInputEvent()
        except:
            pass
        return event
    def setExecuteDeviceGrab(self, newExecuteDeviceGrab = True):
        self.executeDeviceGrab = newExecuteDeviceGrab
    def handleDeviceGrab(self):
        if not self.executeDeviceGrab:
            return
        if self.env['input']['eventBuffer'] != []:
            return
        if not self.noKeyPressed():
            return
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'grabDevices'):
            return
        if self.env['runtime']['screenManager'].getCurrScreenIgnored():
            self.ungrabAllDevices()
        else:
            self.grabAllDevices()
        self.executeDeviceGrab = False 
    def sendKeys(self, keyMacro):
        for e in keyMacro:
            key = ''
            value = 0
            if len(e) != 2:
                continue
            if isinstance(e[0], int) and isinstance(e[1], str):
                key = e[1].upper()
                value = e[0]
            elif isinstance(e[1], int) and isinstance(e[0], str):
                key = e[0].upper()
                value = e[1]
            else:
                continue
            if key.upper() == 'SLEEP':
                time.sleep(value)
            else:
                self.env['runtime']['inputDriver'].sendKey(key, value)
    def handleInputEvent(self, eventData):
        #print(eventData)
        if not eventData:
            return
        # a hang apears.. try to fix
        if self.env['input']['eventBuffer'] == []:
            if self.env['input']['currInput'] != []:
                self.env['input']['currInput'] = []
                self.env['input']['shortcutRepeat'] = 1

        self.env['input']['prevInput'] = self.env['input']['currInput'].copy()
        if eventData['EventState'] == 0:
            if eventData['EventName'] in self.env['input']['currInput']:
                self.env['input']['currInput'].remove(eventData['EventName'])
                if len(self.env['input']['currInput']) > 1:
                    self.env['input']['currInput'] = sorted(self.env['input']['currInput'])
                elif len(self.env['input']['currInput']) == 0:
                    self.env['input']['shortcutRepeat'] = 1 
                self.lastInputTime = time.time()
        elif eventData['EventState'] == 1:
            if not eventData['EventName'] in self.env['input']['currInput']:
                self.env['input']['currInput'].append(eventData['EventName'])
                if len(self.env['input']['currInput']) > 1:
                    self.env['input']['currInput'] = sorted(self.env['input']['currInput'])
                if len(self.lastDeepestInput) < len(self.env['input']['currInput']):
                    self.setLastDeepestInput( self.env['input']['currInput'].copy())
                elif self.lastDeepestInput == self.env['input']['currInput']:
                    if time.time() - self.lastInputTime <= self.env['runtime']['settingsManager'].getSettingAsFloat('keyboard','doubleTapTimeout'):
                        self.env['input']['shortcutRepeat'] += 1
                    else:
                        self.env['input']['shortcutRepeat'] = 1
                self.handleLedStates(eventData)
                self.lastInputTime = time.time()
        elif eventData['EventState'] == 2:
            self.lastInputTime  = time.time()

        self.env['input']['oldNumLock'] = self.env['input']['newNumLock']
        self.env['input']['newNumLock'] = self.env['runtime']['inputDriver'].getLedState()
        self.env['input']['oldCapsLock'] = self.env['input']['newCapsLock'] 
        self.env['input']['newCapsLock'] = self.env['runtime']['inputDriver'].getLedState(1)
        self.env['input']['oldScrollLock'] = self.env['input']['newScrollLock'] 
        self.env['input']['newScrollLock'] = self.env['runtime']['inputDriver'].getLedState(2)
        self.env['runtime']['debug'].writeDebugOut("currInput " + str(self.env['input']['currInput'] ) ,debug.debugLevel.INFO)
        if self.noKeyPressed():
            self.env['input']['prevInput'] = []
            self.handleDeviceGrab()

    def handleLedStates(self, mEvent):
        try:
            if mEvent['EventName'] == 'KEY_NUMLOCK':
                self.env['runtime']['inputDriver'].toggleLedState()             
            elif mEvent['EventName'] == 'KEY_CAPSLOCK':   
                self.env['runtime']['inputDriver'].toggleLedState(1)                           
            elif mEvent['EventName'] == 'KEY_SCROLLLOCK':  
                self.env['runtime']['inputDriver'].toggleLedState(2)               
        except:
            pass
    def grabAllDevices(self):
        if self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'grabDevices'):
            try:
                self.env['runtime']['inputDriver'].grabAllDevices()
            except Exception as e:
                pass                
    def ungrabAllDevices(self):
        if self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'grabDevices'):
            try:
                self.env['runtime']['inputDriver'].ungrabAllDevices()
            except Exception as e:
                pass
    def handlePlugInputDevice(self, eventData):
        self.env['runtime']['inputManager'].updateInputDevices(eventData)
            
    def updateInputDevices(self, newDevice = None):
        try:
            self.env['runtime']['inputDriver'].updateInputDevices(newDevice)  
        except:
            pass
        self.setExecuteDeviceGrab()
        try:
            if self.env['runtime']['screenManager']:
                self.handleDeviceGrab()
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
        try:
            self.env['runtime']['inputDriver'].clearEventBuffer()
        except Exception as e:
            pass
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
        shortcut.append(self.env['input']['shortcutRepeat'])
        if inputSequence:
            shortcut.append(inputSequence)
        else:
            shortcut.append(self.env['input']['currInput'])
        if len(self.env['input']['prevInput']) < len(self.env['input']['currInput']):
            if self.env['input']['shortcutRepeat'] > 1  and not self.shortcutExists(str(shortcut)):
                shortcut = []
                self.env['input']['shortcutRepeat'] = 1
                shortcut.append(self.env['input']['shortcutRepeat'])
                shortcut.append(self.env['input']['currInput'])     
        self.env['runtime']['debug'].writeDebugOut("currShortcut " + str(shortcut) ,debug.debugLevel.INFO)
        return str(shortcut)

    def currKeyIsModifier(self):
        if len(self.getLastDeepestInput()) != 1:
            return False
        return (self.env['input']['currInput'][0] =='KEY_FENRIR') or (self.env['input']['currInput'][0] == 'KEY_SCRIPT')

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
    def loadShortcuts(self, kbConfigPath=fenrirPath + '/../../config/keyboard/desktop.conf'):
        kbConfig = open(kbConfigPath,"r")
        while(True):
            invalid = False
            line = kbConfig.readline()
            if not line:
                break
            line = line.replace('\n','')
            if line.replace(" ","") == '':
                continue
            if line.replace(" ","").startswith("#"):
                continue
            if line.count("=") != 1:
                continue
            sepLine = line.split('=')
            commandName = sepLine[1].upper()
            sepLine[0] = sepLine[0].replace(" ","")
            sepLine[0] = sepLine[0].replace("'","")
            sepLine[0] = sepLine[0].replace('"',"")
            keys = sepLine[0].split(',')
            shortcutKeys = []
            shortcutRepeat = 1
            shortcut = []
            for key in keys:
                try:
                    shortcutRepeat = int(key)
                except:
                    if not self.isValidKey(key.upper()):
                        self.env['runtime']['debug'].writeDebugOut("invalid key : "+ key.upper() + ' command:' +commandName ,debug.debugLevel.WARNING)                    
                        invalid = True
                        break
                    shortcutKeys.append(key.upper()) 
            if invalid:
                continue
            shortcut.append(shortcutRepeat)
            shortcut.append(sorted(shortcutKeys))
            if len(shortcutKeys) != 1 and not 'KEY_FENRIR' in shortcutKeys:
                self.env['runtime']['debug'].writeDebugOut("invalid shortcut (missing KEY_FENRIR): "+ str(shortcut) + ' command:' +commandName ,debug.debugLevel.ERROR)
                continue
            self.env['runtime']['debug'].writeDebugOut("Shortcut: "+ str(shortcut) + ' command:' +commandName ,debug.debugLevel.INFO, onAnyLevel=True)    
            self.env['bindings'][str(shortcut)] = commandName
        kbConfig.close()
        # fix bindings 
        self.env['bindings'][str([1, ['KEY_F1', 'KEY_FENRIR']])] = 'TOGGLE_TUTORIAL_MODE'
    def isValidKey(self, key):
        return key in inputData.keyNames

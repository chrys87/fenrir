#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType
import os, inspect, re, time
currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
fenrirPath = os.path.dirname(currentdir)

class byteManager():
    def __init__(self):
        self.command = ''
        self.switchCtrlModeOnce = 0 
        self.controlMode = True
        self.repeat = 1
        self.lastInputTime = time.time()
        self.lastByteKey = b''
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass
    def unifyEscapeSeq(self, escapeSequence):   
        convertedEscapeSequence = escapeSequence
        if convertedEscapeSequence[0] == 27:
            convertedEscapeSequence = b'^[' + convertedEscapeSequence[1:]
        if len(convertedEscapeSequence) > 1:
            if convertedEscapeSequence[0] == 94 and convertedEscapeSequence[1] ==91:
                convertedEscapeSequence = b'^[' + convertedEscapeSequence[2:]            
        return convertedEscapeSequence
    def handleByteInput(self, eventData):
        if not eventData:
            return
        if eventData == b'':
            return

        convertedEscapeSequence = self.unifyEscapeSeq(eventData)            

        if self.switchCtrlModeOnce > 0:
            self.switchCtrlModeOnce -= 1       
       
        isControlMode = False
        if self.controlMode and not self.switchCtrlModeOnce == 1 or\
          not self.controlMode:
            isControlMode = self.handleControlMode(eventData)

        isCommand = False                
        if self.controlMode and not self.switchCtrlModeOnce == 1 or\
          not self.controlMode and self.switchCtrlModeOnce == 1:
            shortcutData = convertedEscapeSequence
            if self.lastByteKey == convertedEscapeSequence:
                if time.time() - self.lastInputTime <= self.env['runtime']['settingsManager'].getSettingAsFloat('keyboard','doubleTapTimeout'):
                    self.repeat += 1
                    shortcutData = shortcutData + convertedEscapeSequence          
            isCommand = self.detectByteCommand(shortcutData)
            if not isCommand:
                isCommand = self.detectByteCommand(convertedEscapeSequence) 
                self.repeat = 1                                               
        if not (isCommand or isControlMode):
            self.env['runtime']['screenManager'].injectTextToScreen(eventData)
        if not isCommand:
            self.repeat = 1                    
        self.lastByteKey = convertedEscapeSequence
        self.lastInputTime = time.time()
    def handleControlMode(self, escapeSequence): 
        convertedEscapeSequence = self.unifyEscapeSeq(escapeSequence)
        if convertedEscapeSequence == b'^[R':
            self.controlMode = not self.controlMode
            self.switchCtrlModeOnce = 0
            if self.controlMode:
                self.env['runtime']['outputManager'].presentText(_('Sticky Mode On'), soundIcon='Accept', interrupt=True, flush=True)
            else:
                self.env['runtime']['outputManager'].presentText(_('Sticky Mode On'), soundIcon='Cancel', interrupt=True, flush=True)
            return True                
        if convertedEscapeSequence == b'^[:':
            self.switchCtrlModeOnce = 2
            self.env['runtime']['outputManager'].presentText(_('bypass'), soundIcon='PTYBypass', interrupt=True, flush=True)
            return True
        return False          
    def detectByteCommand(self, escapeSequence):
        convertedEscapeSequence = self.unifyEscapeSeq(escapeSequence)
        self.command = self.env['runtime']['inputManager'].getCommandForShortcut(convertedEscapeSequence)
        if self.command != '':        
            self.env['runtime']['eventManager'].putToEventQueue(fenrirEventType.ExecuteCommand, self.command)
            self.command = ''
            return True
        return False        
    def loadByteShortcuts(self, kbConfigPath=fenrirPath + '/../../config/keyboard/pty.conf'):
        kbConfig = open(kbConfigPath,"r")
        while(True):
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
            Values = line.split('=')
            shortcut = bytes(Values[0],'UTF-8')
            commandName = Values[1].upper()
            self.env['bindings'][shortcut] = commandName   
            self.env['runtime']['debug'].writeDebugOut("Byte Shortcut: "+ str(shortcut) + ' command:' +commandName ,debug.debugLevel.INFO, onAnyLevel=True)    
        kbConfig.close()        

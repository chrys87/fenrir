#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import os, inspect, re
currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
fenrirPath = os.path.dirname(currentdir)

class byteManager():
    def __init__(self):
        pass
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

#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class driver():
    def __init__(self):
        self._isInitialized = False
        self.brl = None

    def initialize(self, environment):
        self.env = environment
        try:
            import brlapi
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)                 
            return
            
        try:
            self.connectDevice()            
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('BRAILLE.connectDevice '+str(e),debug.debugLevel.ERROR)         
            return
        self._isInitialized = True
        
    def flush(self):
        if not self._isInitialized:
            return
        try:
            self.brl.writeText('',0)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('BRAILLE.flush '+str(e),debug.debugLevel.ERROR) 
                    
    def writeText(self,text):
        if not self._isInitialized:
            return
        try:
            self.brl.writeText(text)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('BRAILLE.writeText '+str(e),debug.debugLevel.ERROR) 
            
    def connectDevice(self):
        self.brl = brlapi.Connection()
        self.brl.enterTtyModeWithPath()    
    
    def shutdown(self):
        if not self._isInitialized:
            return
        self.brl.leaveTtyMode()       
             

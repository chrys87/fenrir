#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class driver():
    def __init__(self):
        self._isInitialized = False
        self._brl = None

    def initialize(self, environment):
        self.env = environment
        try:
            import brlapi
        except Exception as e:
            print(e)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)                 
            return
            
        try:
            self._brl = brlapi.Connection()  
        except Exception as e:
            print(e)
            self.env['runtime']['debug'].writeDebugOut('BRAILLE.connectDevice '+str(e),debug.debugLevel.ERROR)
            return
        self._isInitialized = True

    def flush(self):
        if not self._isInitialized:
            return
        try:
            self._brl.writeText('',0)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('BRAILLE.flush '+str(e),debug.debugLevel.ERROR)
    
    def writeText(self,text):
        if not self._isInitialized:
            return
        try:
            self._brl.writeText(text)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('BRAILLE.writeText '+str(e),debug.debugLevel.ERROR)

    def connectDevice(self):
        self._brl = brlapi.Connection()

    def enterScreen(self, screen):
        if not self._isInitialized:
            return
        self._brl.enterTtyMode(int(screen))

    def leveScreen(self):
        if not self._isInitialized:
            return
        self._brl.leaveTtyMode()

    def shutdown(self):
        if not self._isInitialized:
            return
        self.leveScreen()

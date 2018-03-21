#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.brailleDriver import brailleDriver

class driver(brailleDriver):
    def __init__(self):
        brailleDriver.__init__(self)
        self._brl = None

    def initialize(self, environment):
        self.env = environment
        try:
            import brlapi
            self._brl = brlapi.Connection()            
            self._deviceSize = self._brl.displaySize           
        except Exception as e:
            print(e)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)                 
            return
        self._isInitialized = True

    def getDeviceSize(self):
        if not self._isInitialized:
            return (0,0)
        if not self._deviceSize:
            return (0,0)
        return self._deviceSize

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

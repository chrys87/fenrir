#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class inputDriver():
    def __init__(self):
        self._initialized = False
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['inputManager'].setShortcutType('KEY')        
        self._isInitialized = True
    def shutdown(self):
        if self._initialized:
            self.removeAllDevices()    
        self._isInitialized = False
    def getInputEvent(self):
        time.sleep(0.1)
        return None
    def clearEventBuffer(self):
        if not self._initialized:
            return    
        del self.env['input']['eventBuffer'][:]
    def updateInputDevices(self, newDevices = None, init = False):
        if not self._initialized:
            return    
    def getLedState(self, led = 0):
        if not self._initialized:
            return False    
        return False
    def toggleLedState(self, led = 0):
        if not self._initialized:
            return
    def grabAllDevices(self):
        if not self._initialized:
            return
    def ungrabAllDevices(self):
        if not self._initialized:
            return
    def hasIDevices(self):
        if not self._initialized:
            return False
        return True
    def removeAllDevices(self):
        if not self._initialized:
            return 
    def sendKey(self):
        if not self._initialized:
            return 
    def __del__(self):
        if not self._initialized:
            return     
        try:
            self.removeAllDevices()
        except:
            pass

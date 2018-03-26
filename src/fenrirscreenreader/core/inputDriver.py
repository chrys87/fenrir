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
            self.releaseDevices()    
        self._isInitialized = False
    def getInputEvent(self):
        time.sleep(0.05)
        return None
    def handleInputEvent(self, event):
        time.sleep(0.05)
        if not self._initialized:
            return
    def writeEventBuffer(self):
        if not self._initialized:
            return    
    def clearEventBuffer(self):
        if not self._initialized:
            return    
        del self.env['input']['eventBuffer'][:]            
    def updateInputDevices(self, force = False, init = False):
        if not self._initialized:
            return    
    def getLedState(self, led = 0):
        if not self._initialized:
            return False    
        return False
    def toggleLedState(self, led = 0):
        if not self._initialized:
            return None
    def grabDevices(self):
        if not self._initialized:
            return None
    def releaseDevices(self):
        if not self._initialized:
            return None
    def __del__(self):
        if not self._initialized:
            return None        
        self.releaseDevices()

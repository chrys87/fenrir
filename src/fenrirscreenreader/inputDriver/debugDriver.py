#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from fenrirscreenreader.core import debug
from fenrirscreenreader.core.inputDriver import inputDriver

class driver(inputDriver):
    def __init__(self):
        inputDriver.__init__(self)
        
    def initialize(self, environment):
        self.env = environment
        self._initialized = True        
        print('Input Debug Driver: Initialized')    
        
    def shutdown(self):
        if self._initialized:
            self.releaseDevices()       
        self._initialized = False    
        print('Input Debug Driver: Shutdown')
        
    def getInputEvent(self):
        time.sleep(0.05)
        if not self._initialized:
            return None
        print('Input Debug Driver: getInputEvent')
        return None
    def writeEventBuffer(self):
        if not self._initialized:
            return    
        print('Input Debug Driver: writeEventBuffer')
    def clearEventBuffer(self):
        if not self._initialized:
            return    
        del self.env['input']['eventBuffer'][:]            
        print('Input Debug Driver: clearEventBuffer')
    def updateInputDevices(self, force = False, init = False):
        if not self._initialized:
            return    
        print('Input Debug Driver: updateInputDevices') 
    def getLedState(self, led = 0):
        if not self._initialized:
            return False    
        return False          
    def toggleLedState(self, led = 0):
        if not self._initialized:
            return    
        print('Input Debug Driver: toggleLedState')
    def grabDevices(self):
        if not self._initialized:
            return    
        print('Input Debug Driver: grabDevices')
    def releaseDevices(self):
        if not self._initialized:
            return    
        print('Input Debug Driver: releaseDevices')
    def __del__(self):
        if self._initialized:
            self.releaseDevices()
        print('Input Debug Driver: __del__')        



#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from core import debug

class driver():
    def __init__(self):
        self._initialized = False
        
    def initialize(self, environment):
        self.env = environment
        
    def shutdown(self):
        pass
        
    def getInputEvent(self):
        time.sleep(0.05)
        if not self._initialized:
            return None

    def writeEventBuffer(self):
        if not self._initialized:
            return    

    def clearEventBuffer(self):
        if not self._initialized:
            return    

    def getInputDevices(self):
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



#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class soundDriver():
    def __init__(self):
        self.volume = 1.0
        self._initialized = False

    def initialize(self, environment):
        self.env = environment
        self._initialized = True

    def shutdown(self):
        if not self._initialized:
            return
        self.cancel()
        self._isInitialized = False            

    def playFrequence(self, frequence = 1000, duration = 0.3, adjustVolume = 0):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
      

    def playSoundFile(self, filePath, interrupt = True):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()            

    def cancel(self):
        if not self._initialized:
            return

    def setCallback(self, callback):
        if not self._initialized:
            return

    def setVolume(self, volume):
        if not self._initialized:
            return    
        self.volume = volume

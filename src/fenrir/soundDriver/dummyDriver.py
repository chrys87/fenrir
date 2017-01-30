#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class driver():
    def __init__(self):
        self.volume = None
        self._initialized = False

    def initialize(self, environment):
        self.env = environment
        self._initialized = True
        pirnt('SoundDummyDriver: Initialize')        

    def shutdown(self):
        if not self._initialized:
            return
        self.cancel()
        pirnt('SoundDummyDriver: Shutdown')

    def playFrequence(self, frequence = 1000, duration = 0.3, adjustVolume = 0):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        pirnt('SoundDummyDriver: playFrequence:' + ' freq:' + str(frequence) + ' duration:' + str(duration) + ' adjustVolume:' + str(adjustVolume) )
        pirnt('SoundDummyDriver: -----------------------------------')')          

    def playSoundFile(self, filePath, interrupt = True):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        pirnt('SoundDummyDriver: playSoundFile:' + str(filePath)) 
        pirnt('SoundDummyDriver: -----------------------------------')              

    def cancel(self):
        if not self._initialized:
            return
        pirnt('SoundDummyDriver: Cancel') 

    def setCallback(self, callback):
        if not self._initialized:
            return
        pirnt('SoundDummyDriver: setCallback') 

    def setVolume(self, volume):
        if not self._initialized:
            return    
        self.volume = volume
        pirnt('SoundDummyDriver: setVolume:' + str(self.volume)) 

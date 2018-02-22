#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrir.core import debug

class driver():
    def __init__(self):
        self.volume = None
        self._initialized = False

    def initialize(self, environment):
        self.env = environment
        self._initialized = True
        print('SoundDummyDriver: Initialize')        

    def shutdown(self):
        if not self._initialized:
            return
        self.cancel()
        print('SoundDummyDriver: Shutdown')

    def playFrequence(self, frequence = 1000, duration = 0.3, adjustVolume = 0):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        print('SoundDummyDriver: playFrequence:' + ' freq:' + str(frequence) + ' duration:' + str(duration) + ' adjustVolume:' + str(adjustVolume) )
        print('SoundDummyDriver: -----------------------------------')          

    def playSoundFile(self, filePath, interrupt = True):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        print('SoundDummyDriver: playSoundFile:' + str(filePath)) 
        print('SoundDummyDriver: -----------------------------------')              

    def cancel(self):
        if not self._initialized:
            return
        print('SoundDummyDriver: Cancel') 

    def setCallback(self, callback):
        if not self._initialized:
            return
        print('SoundDummyDriver: setCallback') 

    def setVolume(self, volume):
        if not self._initialized:
            return    
        self.volume = volume
        print('SoundDummyDriver: setVolume:' + str(self.volume)) 

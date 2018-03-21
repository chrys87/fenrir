#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.soundDriver import soundDriver

class driver(soundDriver):
    def __init__(self):
        soundDriver.__init__(self)

    def initialize(self, environment):
        self.env = environment
        self._initialized = True
        print('Sound Debug Driver: Initialized')        

    def shutdown(self):
        if not self._initialized:
            return
        self.cancel()
        self._initialized = False        
        print('Sound Debug Driver: Shutdown')

    def playFrequence(self, frequence = 1000, duration = 0.3, adjustVolume = 0):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        print('Sound Debug Driver: playFrequence:' + ' freq:' + str(frequence) + ' duration:' + str(duration) + ' adjustVolume:' + str(adjustVolume) )
        print('Sound Debug Driver: -----------------------------------')          

    def playSoundFile(self, filePath, interrupt = True):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        print('Sound Debug Driver: playSoundFile:' + str(filePath)) 
        print('Sound Debug Driver: -----------------------------------')              

    def cancel(self):
        if not self._initialized:
            return
        print('Sound Debug Driver: Cancel') 

    def setCallback(self, callback):
        if not self._initialized:
            return
        print('Sound Debug Driver: setCallback') 

    def setVolume(self, volume):
        if not self._initialized:
            return    
        self.volume = volume
        print('Sound Debug Driver: setVolume:' + str(self.volume)) 

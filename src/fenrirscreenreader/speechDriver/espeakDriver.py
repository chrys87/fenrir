#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# Espeak driver

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.speechDriver import speechDriver

class driver(speechDriver):
    def __init__(self):
        speechDriver.__init__(self)
        self._es = None

    def initialize(self, environment):
        self.env = environment          
        try:
            from espeak import espeak 
            self._es = espeak
            self._isInitialized = True
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)         
            self._initialized = False

    def speak(self,text, interrupt=True):
        if not self._isInitialized:
            return
        if not interrupt:
            self.cancel()
        if self.language != None:
            if self.language != '':
                self._es.set_voice(self.language)   
        elif self.voice != None:
            if self.voice != '':                
                self._es.set_voice(self.voice)         
        self._es.synth(text)

    def cancel(self):
        if not self._isInitialized:
            return
        self._es.cancel()
        return

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        return self._es.set_parameter(self._es.Parameter().Pitch, int(pitch * 99)) 
        
    def setRate(self, rate):
        if not self._isInitialized:
            return
        return self._es.set_parameter(self._es.Parameter().Rate, int(rate * 899 + 100))

    def setVolume(self, volume):
        if not self._isInitialized:
            return    
        return self._es.set_parameter(self._es.Parameter().Volume, int(volume * 200))

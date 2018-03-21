#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class speechDriver():
    def __init__(self):
        self._isInitialized = False
        self.language = None
        self.voice = None
        self.module = None
        self.pitch = None
        self.rate = None
        self.volume = None
    def initialize(self, environment):
        self.env = environment
        self._isInitialized = True        
        
    def shutdown(self):
        if self._isInitialized:
            self.cancel()
        self._isInitialized = False            

    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return
        if not queueable: 
            self.cancel()
    
    def cancel(self):
        if not self._isInitialized:
            return     

    def setCallback(self, callback):
        if not self._isInitialized:
            return        
        if not callback:
            return

    def clear_buffer(self):
        if not self._isInitialized:
            return

    def setVoice(self, voice):
        if not self._isInitialized:
            return
        if voice == '':
            return            
        self.voice = voice 

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        if not isinstance(pitch, float):
            return
        if pitch < 0.0:
            retrun
        if pitch > 1.0:
            return
        self.pitch = pitch
    def setRate(self, rate):
        if not self._isInitialized:
            return
        if not isinstance(rate, float):
            return
        if rate < 0.0:
            retrun
        if rate > 1.0:
            return
        self.rate = rate
    def setModule(self, module):
        if not self._isInitialized:
            return
        if not isinstance(module, str):
            return
        if module == '':
            return            
        self.module = module

    def setLanguage(self, language):
        if not self._isInitialized:
            return
        if not isinstance(language, str):
            return
        if language == '':
            return            
        self.language = language 
    def setVolume(self, volume):
        if not self._isInitialized:
            return     
        if not isinstance(volume,float):
            return
        if volume < 0.0:
            retrun
        if volume > 1.0:
            return
        self.volume = volume

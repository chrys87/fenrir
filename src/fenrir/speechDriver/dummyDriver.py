#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# generic driver

from core import debug

class driver():
    def __init__(self):
        pass
    def initialize(self, environment):
        self._isInitialized = True
        self.env = environment
        pirnt('SpeechDummyDriver: Iitialize')
        
    def shutdown(self):
        pirnt('SpeechDummyDriver: Shutdown')

    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return
        if not queueable: 
            self.cancel()
        pirnt('SpeechDummyDriver: Speak:'+text)
        pirnt('SpeechDummyDriver: -----------------------------------')

    def cancel(self):
        if not self._isInitialized:
            return
        pirnt('SpeechDummyDriver: Cancel')        

    def setCallback(self, callback):
        pirnt('SpeechDummyDriver: setCallback')    

    def clear_buffer(self):
        if not self._isInitialized:
            return
        pirnt('SpeechDummyDriver: clear_buffer')    

    def setVoice(self, voice):
        if not self._isInitialized:
            return
        pirnt('SpeechDummyDriver: setVoice:' +  str(voice))    

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        pirnt('SpeechDummyDriver: setPitch:' + str(pitch))    

    def setRate(self, rate):
        if not self._isInitialized:
            return
        pirnt('SpeechDummyDriver: setRate:' + str(rate))    

    def setModule(self, module):
        if not self._isInitialized:
            return 
        pirnt('SpeechDummyDriver: setModule:' + str(module))    

    def setLanguage(self, language):
        if not self._isInitialized:
            return
        pirnt('SpeechDummyDriver: setLanguage:' + str(language))    

    def setVolume(self, volume):
        if not self._isInitialized:
            return     
        pirnt('SpeechDummyDriver: setVolume:' + str(volume))

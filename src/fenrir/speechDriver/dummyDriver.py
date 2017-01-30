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
        print('SpeechDummyDriver: Iitialize')
        
    def shutdown(self):
        print('SpeechDummyDriver: Shutdown')

    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return
        if not queueable: 
            self.cancel()
        print('SpeechDummyDriver: Speak:'+text)
        print('SpeechDummyDriver: -----------------------------------')

    def cancel(self):
        if not self._isInitialized:
            return
        print('SpeechDummyDriver: Cancel')        

    def setCallback(self, callback):
        print('SpeechDummyDriver: setCallback')    

    def clear_buffer(self):
        if not self._isInitialized:
            return
        print('SpeechDummyDriver: clear_buffer')    

    def setVoice(self, voice):
        if not self._isInitialized:
            return
        print('SpeechDummyDriver: setVoice:' +  str(voice))    

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        print('SpeechDummyDriver: setPitch:' + str(pitch))    

    def setRate(self, rate):
        if not self._isInitialized:
            return
        print('SpeechDummyDriver: setRate:' + str(rate))    

    def setModule(self, module):
        if not self._isInitialized:
            return 
        print('SpeechDummyDriver: setModule:' + str(module))    

    def setLanguage(self, language):
        if not self._isInitialized:
            return
        print('SpeechDummyDriver: setLanguage:' + str(language))    

    def setVolume(self, volume):
        if not self._isInitialized:
            return     
        print('SpeechDummyDriver: setVolume:' + str(volume))

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# speech-dispatcher driver

from core import debug

class driver():
    def __init__(self):
        self._sd = None
        self._isInitialized = False
        self._language = ''

    def initialize(self, environment):
        self.env = environment
        try:
            import speechd 
            self._sd =  speechd.SSIPClient('fenrir')
            self._punct = speechd.PunctuationMode()
            self._isInitialized = True
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)         
            self._initialized = False
                    
    def shutdown(self):
        if not self._isInitialized:
            return
        self._isInitialized = False
        self.cancel()
        try:
            self._sd.close()
        except:
            pass
        
    def speak(self,text, queueable=True):
        if not self._isInitialized:
            self.initialize(self.env)
            if not self._isInitialized:
                return False
        try:
            if queueable == False: self.cancel()        
            self._sd.set_synthesis_voice(self._language)        
            self._sd.set_punctuation(self._punct.NONE)              
            self._sd.speak(text)            
        except Exception as e:
            self._isInitialized = False

    def cancel(self):
        if not self._isInitialized:
            return
        self._sd.cancel()

    def setCallback(self, callback):
        pass
    
    def clear_buffer(self):
        if not self._isInitialized:
            return

    def setVoice(self, voice):
        if not self._isInitialized:
            return
        try:
            if voice != '':
                self._sd.set_voice(voice)
        except:
            pass

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        try:
            self._sd.set_pitch(int(-100 + pitch * 200)) 
        except:
            pass

    def setRate(self, rate):
        if not self._isInitialized:
            return 
        try:
            self._sd.set_rate(int(-100 + rate * 200))
        except:
            pass

    def setModule(self, module):
        if not self._isInitialized:
            return
        try:
            self._sd.set_output_module(module)
        except:
            pass
            
    def setLanguage(self, language):
        if not self._isInitialized:
            return    
        self._language = language
        
    def setVolume(self, volume):
        if not self._isInitialized:
            return 
        try:               
            self._sd.set_volume(int(-100 + volume * 200))
        except:
            pass

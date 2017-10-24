#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# generic driver

from core import debug

class speechDriver():
    def __init__(self):
        self._isInitialized = False
        self.language = None
        self.voice = None
        self.module = None
    def initialize(self, environment):
        self.env = environment
        self._isInitialized = True        
        
    def shutdown(self):
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
        pass

    def clear_buffer(self):
        if not self._isInitialized:
            return

    def setVoice(self, voice):
        if not self._isInitialized:
            return
        if voice =='':
            return            
        self.voice = voice 

    def setPitch(self, pitch):
        if not self._isInitialized:
            return

    def setRate(self, rate):
        if not self._isInitialized:
            return

    def setModule(self, module):
        if not self._isInitialized:
            return
        if module =='':
            return            
        self.module = module

    def setLanguage(self, language):
        if not self._isInitialized:
            return
        if language =='':
            return            
        self.language = language 
    def setVolume(self, volume):
        if not self._isInitialized:
            return     

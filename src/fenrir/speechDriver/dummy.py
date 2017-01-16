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
        self._isInitialized = False 
        self.env = environment   
    def shutdown(self):
        pass

    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return False
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

    def setPitch(self, pitch):
        if not self._isInitialized:
            return 

    def setRate(self, rate):
        if not self._isInitialized:
            return 

    def setModule(self, module):
        if not self._isInitialized:
            return 

    def setLanguage(self, language):
        if not self._isInitialized:
            return

    def setVolume(self, volume):
        if not self._isInitialized:
            return     

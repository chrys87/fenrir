#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# generic driver

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.speechDriver import speechDriver

class driver(speechDriver):
    def __init__(self):
        speechDriver.__init__(self)
    def initialize(self, environment):
        self._isInitialized = True
        self.env = environment
        print('Speech Debug Driver: Iitialized')
        
    def shutdown(self):
        if self._isInitialized:
            self.cancel()
        self._isInitialized = False    
        print('Speech Debug Driver: Shutdown')

    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return
        if not queueable: 
            self.cancel()
        print('Speech Debug Driver: Speak:'+text)
        print('Speech Debug Driver: -----------------------------------')

    def cancel(self):
        if not self._isInitialized:
            return
        print('Speech Debug Driver: Cancel')        

    def setCallback(self, callback):
        print('Speech Debug Driver: setCallback')    

    def clear_buffer(self):
        if not self._isInitialized:
            return
        print('Speech Debug Driver: clear_buffer')    

    def setVoice(self, voice):
        if not self._isInitialized:
            return
        print('Speech Debug Driver: setVoice:' +  str(voice))    

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        print('Speech Debug Driver: setPitch:' + str(pitch))    

    def setRate(self, rate):
        if not self._isInitialized:
            return
        print('Speech Debug Driver: setRate:' + str(rate))    

    def setModule(self, module):
        if not self._isInitialized:
            return 
        print('Speech Debug Driver: setModule:' + str(module))    

    def setLanguage(self, language):
        if not self._isInitialized:
            return
        print('Speech Debug Driver: setLanguage:' + str(language))    

    def setVolume(self, volume):
        if not self._isInitialized:
            return     
        print('Speech Debug Driver: setVolume:' + str(volume))

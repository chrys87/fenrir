#!/usr/bin/python

# generic driver

class driver():
    def __init__(self ):
        pass
    def initialize(self, environment):
        self._isInitialized = False
        return environment    
    def shutdown(self, environment):
        return environment

    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return False
        if not queueable: 
            self.cancel()
        return True

    def cancel(self):
        if not self._isInitialized:
            return False
        return True

    def setCallback(self, callback):
        pass

    def clear_buffer(self):
        if not self._isInitialized:
            return False
        return True

    def setVoice(self, voice):
        if not self._isInitialized:
            return False
        return True

    def setPitch(self, pitch):
        if not self._isInitialized:
            return False
        return True

    def setRate(self, rate):
        if not self._isInitialized:
            return False
        return True

    def setModule(self, module):
        if not self._isInitialized:
            return False

    def setLanguage(self, language):
        if not self._isInitialized:
            return False
        return True

    def setVolume(self, volume):
        if not self._isInitialized:
            return False    
        return True

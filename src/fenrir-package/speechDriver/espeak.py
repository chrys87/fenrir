#!/usr/bin/python

# Espeak driver

class driver():
    def __init__(self ):
        self._es = None
        self._isInitialized = False
        try:
            from espeak import espeak 
            self._es = espeak
            self._isInitialized = True
        except:
            self._initialized = False
    def initialize(self, environment):
        return environment            
    def shutdown(self, environment):
        return environment

    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return False
        if not queueable:
            self.cancel()
        self._es.synth(text)
        return True

    def cancel(self):
        if not self._isInitialized:
            return False
        self._es.cancel()
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
        return self._es.set_voice(voice)

    def setPitch(self, pitch):
        if not self._isInitialized:
            return False

    def setRate(self, rate):
        if not self._isInitialized:
            return False
        return self._es.set_parameter(self._es.Parameter().Rate, int(rate*450 + 80))

        return self._es.set_parameter(self._es.Parameter().Pitch, int(pitch * 99)) 
    def setModule(self, module):
        if not self._isInitialized:
            return False

    def setLanguage(self, language):
        if not self._isInitialized:
            return False
        return self._es.set_voice(language)

    def setVolume(self, volume):
        if not self._isInitialized:
            return False    
        return self._es.set_parameter(self._es.Parameter().Volume, int(volume * 200))

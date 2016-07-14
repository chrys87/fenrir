#!/usr/bin/python

# Espeak driver

class speech():
    def __init__(self, ):
        self._es = None
        self._isInitialized = False
        try:
            from espeak import espeak 
            self._es = espeak
            self._isInitialized = True
        except:
            self._initialized = False


    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return False
        if queueable == False: self.cancel()
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
        return self._es.set_parameter(self._es.Parameter().Pitch, pitch) 

    def setSpeed(self, speed):
        if not self._isInitialized:
            return False
        return self._es.set_parameter(self._es.Parameter().Rate, speed) 

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
        return self._es.set_parameter(self._es.Parameter().Volume, volume)     

    def shutdown(self):
        pass

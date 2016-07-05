#!/usr/bin/python

# Espeak driver

class speech():
    def __init__(self, ):
        self.es = None
        self.isInitialized = False
        try:
            from espeak import espeak 
            self.es = espeak
            self.isInitialized = True
        except:
            self.initialized = False


    def speak(self,text, queueable=True):
        if not self.isInitialized:
            return False
        if queueable == False: self.cancel()
        self.es.synth(text)
        return True

    def cancel(self):
        if not self.isInitialized:
            return False
        self.es.cancel()
        return True

    def clear_buffer(self):
        if not self.isInitialized:
            return False
        return True

    def setVoice(self, voice):
        if not self.isInitialized:
            return False
        return es.set_voice('de')

    def setPitch(self, pitch):
        if not self.isInitialized:
            return False
        return es.set_parameter(espeak.Parameter.Pitch, pitch) 

    def setSpeed(self, speed):
        if not self.isInitialized:
            return False
        return es.set_parameter(espeak.Parameter.Rate, speed) 

    def setModule(self, module):
        pass

    def shutdown(self):
        pass

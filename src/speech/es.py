#!/usr/bin/python

# Espeak driver

class speech():
    def __init__(self, ):
        self.es = None
        self.isInitialized = False
#        try:
        from espeak import espeak 
        self.es = espeak
        self.isInitialized = True
#        except:
#            self.initialized = False


    def speak(self,text, queueable=True):
        if queueable == False: self.stop()
        self.es.synth(text)

    def stop(self):
        self.es.cancel()

    def clear_buffer(self):
        pass

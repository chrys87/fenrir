#!/usr/bin/python

# speech-dispatcher driver

class driver():
    def __init__(self ):
        self._sd = None
        self._isInitialized = False
        self._language = ''
        try:
            import speechd 
            self._sd =  speechd.SSIPClient('fenrir')
            self._isInitialized = True
        except:
            self._initialized = False
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        if not self._isInitialized:
            return environment
        self._isInitialized = False
        self.cancel()
        self._sd.close()
        return environment
        
    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return False
        if queueable == False: self.cancel()
        try:
            self._sd.set_synthesis_voice(self._language)        
        except:
            pass
        self._sd.speak(text)
        return True

    def cancel(self):
        if not self._isInitialized:
            return False
        self._sd.cancel()
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
        try:
            if voice != '':
                self._sd.set_voice(voice)
            return True
        except:
            return False

    def setPitch(self, pitch):
        if not self._isInitialized:
            return False
        try:
            self._sd.set_pitch(int(-100 + pitch * 200)) 
            return True
        except:
            return False

    def setRate(self, rate):
        if not self._isInitialized:
            return False
        try:
            self._sd.set_rate(int(-100 + rate * 200))
            return True
        except:
            return False

    def setModule(self, module):
        if not self._isInitialized:
            return False
        try:
            self._sd.set_output_module(module)
            return True
        except:
            return False
            
    def setLanguage(self, language):
        if not self._isInitialized:
            return False    
        self._language = language
        
    def setVolume(self, volume):
        if not self._isInitialized:
            return False    
        self._sd.set_volume(int(-100 + volume * 200))


#!/usr/bin/python

# speech-dispatcher driver

class speech():
    def __init__(self ):
        self._sd = None
        self._isInitialized = False
        try:
            import speechd 
            self._sd =  speechd.SSIPClient('fenrir')
            self._isInitialized = True
        except:
            self._initialized = False


    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return False
        if queueable == False: self.cancel()
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
            self._sd.set_voice(voice)
            return True
        except:
            return False

    def setPitch(self, pitch):
        if not self._isInitialized:
            return False
        try:
            self._sd.set_pitch(pitch) 
            return True
        except:
            return False

    def setSpeed(self, speed):
        if not self._isInitialized:
            return False
        try:
            self._sd.set_rate(speed)
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
        self._sd.set_language(language)
        
    def shutdown(self):
        if not self._isInitialized:
            return False
        self._isInitialized = False
        self.cancel()
        self._sd.close()
        return True

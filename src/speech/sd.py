#!/usr/bin/python

# speech-dispatcher driver

class speech():
    def __init__(self, ):
        self.sd = None
        self.isInitialized = False
        try:
            import speechd 
            self.sd =  speechd.SSIPClient('fenrir')
            self.isInitialized = True
        except:
            self.initialized = False


    def speak(self,text, queueable=True):
        if not self.isInitialized:
            return False
        if queueable == False: self.cancel()
        self.sd.speak(text)
        return True

    def cancel(self):
        if not self.isInitialized:
            return False
        self.sd.cancel()
        return True

    def clear_buffer(self):
        if not self.isInitialized:
            return False
        return True

    def setVoice(self, voice):
        if not self.isInitialized:
            return False
        try:
            self.sd.set_voice(voice)
            return True
        except:
            return False

    def setPitch(self, pitch):
        if not self.isInitialized:
            return False
        try:
            self.sd.set_pitch(pitch) 
            return True
        except:
            return False

    def setSpeed(self, speed):
        if not self.isInitialized:
            return False
        try:
            self.sd.set_rate(speed)
            return True
        except:
            return False

    def shutdown(self):
        self.cancel()
        self.sd.close()

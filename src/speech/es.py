#!/usr/bin/python

# Espeak driver

class speech():
    isInitialized = False
    
    def __init__(self):
        try:
            pass
            isInitialized = True
        except:
            initialized = False

    def speak(text, queueable=True):
        if queueable == False: self.stop()

    def stop(self):
        pass

    def clear_buffer(self):
        pass

#!/usr/bin/python

# Generic speech driver

class speech():
    def __init__(self, ):
        self.gn = None
        self.isInitialized = False
#        try:


    def speak(self,text, queueable=True):
        if queueable == False: self.stop()
        self.gn.synth(text)

    def stop(self):
        self.gn.cancel()

    def clear_buffer(self):
        pass

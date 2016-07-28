#!/bin/python
import subprocess

class sound():
    def __init__(self):
        pass
    def playFrequence(self, frequence, duration, adjustVolume):
        pass
    def playSoundFile(self, filePath, interrupt = True):
         subprocess.call("play " + filePath, shell=True)
    def cancel(self):
        pass        
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

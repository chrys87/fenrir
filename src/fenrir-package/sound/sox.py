#!/bin/python
import subprocess

class sound():
    def __init__(self):
        pass
    def playFrequence(self, frequence, duration, adjustVolume):
        pass
    def playSoundFile(self, filePath, interrupt = True):
        self.proc = subprocess.Popen("play -q " + filePath, shell=True)
    def cancel(self):
        pass        
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

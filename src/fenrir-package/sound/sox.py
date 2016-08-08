#!/bin/python
import subprocess

class sound():
    def __init__(self):
        self.volume = 1.0;
    def playFrequence(self, frequence, duration, adjustVolume):
        pass
    def playSoundFile(self, filePath, interrupt = True):
        self.proc = subprocess.Popen("play -q -v " + str(self.volume ) + ' ' + filePath, shell=True)
    def cancel(self):
        pass        
    def setCallback(self, callback):
        pass
    def setVolume(self, volume):
        self.volume = volume        
    def shutdown(self):
        pass

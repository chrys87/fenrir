#!/bin/python
import subprocess

class driver():
    def __init__(self):
        self.proc = None
        self.volume = 1.0
        self.soundType = ''
        self.soundFileCommand = 'play -q -v fenrirVolume fenrirSoundFile'
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment
    def playFrequence(self, frequence, duration, adjustVolume):
        self.soundType = 'frequence'
    def playSoundFile(self, filePath, interrupt = True):
        if interrupt:
            self.cancel()
        popenSoundFileCommand = self.soundFileCommand.replace('fenrirVolume', str(self.volume ))
        popenSoundFileCommand = popenSoundFileCommand.replace('fenrirSoundFile', filePath)
        self.proc = subprocess.Popen(popenSoundFileCommand filePath, shell=True)
        self.soundType = 'file'
    def cancel(self):
        if self.soundType == 'file':
            self.proc.kill()
        self.soundType = ''
    def setCallback(self, callback):
        pass
    def setVolume(self, volume):
        self.volume = volume        

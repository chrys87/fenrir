#!/bin/python
import subprocess

class driver():
    def __init__(self):
        self.proc = None
        self.volume = 1.0
        self.soundType = ''
        self.soundFileCommand = ''
        self.frequenceCommand = ''
    def initialize(self, environment):
        self.soundFileCommand = environment['runtime']['settingsManager'].getSetting(environment,'sound', 'genericPlayFileCommand')
        self.frequenceCommand = environment['runtime']['settingsManager'].getSetting(environment,'sound', 'genericFrequencyCommand')
        return environment
    def shutdown(self, environment):
        return environment
    def playFrequence(self, frequence, duration, adjustVolume):
        if interrupt:
            self.cancel()
        popenFrequenceCommand = self.frequenceCommand.replace('fenrirVolume', str(self.volume + adjustVolume ))
        popenFrequenceCommand = popenFrequenceCommand.replace('fenrirFreqDuration', str(duration))
        popenFrequenceCommand = popenFrequenceCommand.replace('fenrirFrequence', str(frequence))        
        self.proc = subprocess.Popen(popenFrequenceCommand, shell=True)
        self.soundType = 'frequence'
    def playSoundFile(self, filePath, interrupt = True):
        if interrupt:
            self.cancel()
        popenSoundFileCommand = self.soundFileCommand.replace('fenrirVolume', str(self.volume ))
        popenSoundFileCommand = popenSoundFileCommand.replace('fenrirSoundFile', filePath)
        self.proc = subprocess.Popen(popenSoundFileCommand, shell=True)
        self.soundType = 'file'
    def cancel(self):
        if self.soundType == 'file':
            self.proc.kill()
        self.soundType = ''
    def setCallback(self, callback):
        pass
    def setVolume(self, volume):
        self.volume = volume        

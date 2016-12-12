#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import subprocess

class driver():
    def __init__(self):
        self.proc = None
        self.volume = 1.0
        self.soundType = ''
        self.soundFileCommand = ''
        self.frequenceCommand = ''
        self._initialized = False        
    def initialize(self, environment):
        self.env = environment
        self.soundFileCommand = self.env['runtime']['settingsManager'].getSetting('sound', 'genericPlayFileCommand')
        self.frequenceCommand = self.env['runtime']['settingsManager'].getSetting('sound', 'genericFrequencyCommand')
        if self.soundFileCommand == '':
            self.soundFileCommand = 'play -q -v fenrirVolume fenrirSoundFile'
        if self.frequenceCommand == '':
            self.frequenceCommand = 'play -q -v fenrirVolume -n -c1 synth fenrirDuration sine fenrirFrequence'
        self._initialized = True
    def shutdown(self):
        if not self._initialized:
            return    
        self.cancel()
    def playFrequence(self, frequence = 1000, duration = 0.3, adjustVolume = 0):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        popenFrequenceCommand = self.frequenceCommand.replace('fenrirVolume', str(self.volume + adjustVolume ))
        popenFrequenceCommand = popenFrequenceCommand.replace('fenrirFreqDuration', str(duration))
        popenFrequenceCommand = popenFrequenceCommand.replace('fenrirFrequence', str(frequence))        
        self.proc = subprocess.Popen(popenFrequenceCommand, shell=True)
        self.soundType = 'frequence'
    def playSoundFile(self, filePath, interrupt = True):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        popenSoundFileCommand = self.soundFileCommand.replace('fenrirVolume', str(self.volume ))
        popenSoundFileCommand = popenSoundFileCommand.replace('fenrirSoundFile', filePath)
        self.proc = subprocess.Popen(popenSoundFileCommand, shell=True)
        self.soundType = 'file'
    def cancel(self):
        if not self._initialized:
            return    
        if self.soundType == '':
            return
        if self.soundType == 'file':
            self.proc.kill()
        if self.soundType == 'frequence':
            self.proc.kill()            
        self.soundType = ''
    def setCallback(self, callback):
        if not self._initialized:
            return
    def setVolume(self, volume):
        if not self._initialized:
            return    
        self.volume = volume        

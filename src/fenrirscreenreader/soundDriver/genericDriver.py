#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import subprocess
import shlex
from fenrirscreenreader.core.soundDriver import soundDriver

class driver(soundDriver):
    def __init__(self):
        soundDriver.__init__(self)
        self.proc = None
        self.soundType = ''
        self.soundFileCommand = ''
        self.frequenceCommand = ''
    def initialize(self, environment):
        self.env = environment
        self.soundFileCommand = self.env['runtime']['settingsManager'].getSetting('sound', 'genericPlayFileCommand')
        self.frequenceCommand = self.env['runtime']['settingsManager'].getSetting('sound', 'genericFrequencyCommand')
        if self.soundFileCommand == '':
            self.soundFileCommand = 'play -q -v fenrirVolume fenrirSoundFile'
        if self.frequenceCommand == '':
            self.frequenceCommand = 'play -q -v fenrirVolume -n -c1 synth fenrirDuration sine fenrirFrequence'
        self._initialized = True

    def playFrequence(self, frequence = 1000, duration = 0.3, adjustVolume = 0):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        popenFrequenceCommand = shlex.split(self.frequenceCommand)
        for idx, word in enumerate(popenFrequenceCommand):
            word = word.replace('fenrirVolume', str(self.volume + adjustVolume ))
            word = word.replace('fenrirFreqDuration', str(duration))
            word = word.replace('fenrirFrequence', str(frequence))
            popenFrequenceCommand[idx] = word        
        self.proc = subprocess.Popen(popenFrequenceCommand, stdin=None, stdout=None, stderr=None, shell=False)
        self.soundType = 'frequence'
    def playSoundFile(self, filePath, interrupt = True):
        if not self._initialized:
            return    
        if interrupt:
            self.cancel()
        popenSoundFileCommand = shlex.split(self.soundFileCommand)
        for idx, word in enumerate(popenSoundFileCommand):
            word = word.replace('fenrirVolume', str(self.volume ))
            word = word.replace('fenrirSoundFile', str(filePath))
            popenSoundFileCommand[idx] = word                
        self.proc = subprocess.Popen(popenSoundFileCommand, shell=False)
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

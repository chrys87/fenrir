#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class driver():
    def __init__(self):
        self.volume = None
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        self.cancel()
    def playFrequence(self, frequence = 1000, duration = 0.3, adjustVolume = 0):
        if interrupt:
            self.cancel()
    def playSoundFile(self, filePath, interrupt = True):
        if interrupt:
            self.cancel()
    def cancel(self):
        pass
    def setCallback(self, callback):
        pass
    def setVolume(self, volume):
        self.volume = volume        

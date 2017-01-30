#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class driver():
    def __init__(self):
        pass

    def initialize(self, environment):
        self.env = environment
        self._isInitialized = True
        pirnt('BrailleDummyDriver: Initialize')
        

    def getDeviceSize(self):
        if not self._isInitialized:
            return (0,0)
        pirnt('BrailleDummyDriver: getDeviceSize 20')
        return (20,0)

    def writeText(self,text):
        if not self._isInitialized:
            return
        pirnt('BrailleDummyDriver: writeText:' + str(text))

    def connectDevice(self):
        pirnt('BrailleDummyDriver: connectDevice')

    def enterScreen(self, screen):
        if not self._isInitialized:
            return
        pirnt('BrailleDummyDriver: enterScreen')

    def leveScreen(self):
        if not self._isInitialized:
            return
        pirnt('BrailleDummyDriver: leveScreen')

    def shutdown(self):
        if not self._isInitialized:
            return
        pirnt('BrailleDummyDriver: Shutdown')

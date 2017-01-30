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
        print('BrailleDummyDriver: Initialize')
        

    def getDeviceSize(self):
        if not self._isInitialized:
            return (0,0)
        print('BrailleDummyDriver: getDeviceSize 20')
        return (20,0)

    def writeText(self,text):
        if not self._isInitialized:
            return
        print('BrailleDummyDriver: writeText:' + str(text))
        print('BrailleDummyDriver: -----------------------------------')

    def connectDevice(self):
        print('BrailleDummyDriver: connectDevice')

    def enterScreen(self, screen):
        if not self._isInitialized:
            return
        print('BrailleDummyDriver: enterScreen')

    def leveScreen(self):
        if not self._isInitialized:
            return
        print('BrailleDummyDriver: leveScreen')

    def shutdown(self):
        if not self._isInitialized:
            return
        print('BrailleDummyDriver: Shutdown')

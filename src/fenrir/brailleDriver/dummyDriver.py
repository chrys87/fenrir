#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class driver():
    def __init__(self):
        self.printMessages = False

    def initialize(self, environment):
        self.env = environment
        self._isInitialized = True
        self.deviceSize = (40,0)
        if self.printMessages:
            print('BrailleDummyDriver: Initialize')
        

    def getDeviceSize(self):
        if not self._isInitialized:
            return (0,0)
        if self.printMessages:
            print('BrailleDummyDriver: getDeviceSize ' + str(self.deviceSize))
        return self.deviceSize

    def writeText(self,text):
        if not self._isInitialized:
            return
        if self.printMessages:
            print('BrailleDummyDriver: writeText:' + str(text))
            print('BrailleDummyDriver: -----------------------------------')

    def connectDevice(self):
        if self.printMessages:
            print('BrailleDummyDriver: connectDevice')

    def enterScreen(self, screen):
        if not self._isInitialized:
            return
        if self.printMessages:
            print('BrailleDummyDriver: enterScreen')

    def leveScreen(self):
        if not self._isInitialized:
            return
        if self.printMessages:
            print('BrailleDummyDriver: leveScreen')

    def shutdown(self):
        if not self._isInitialized:
            return
        if self.printMessages:
            print('BrailleDummyDriver: Shutdown')

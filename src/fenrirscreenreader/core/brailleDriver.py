#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class brailleDriver():
    def __init__(self):
        self._isInitialized = False
        self.deviceSize = None
    def initialize(self, environment):
        self.env = environment
        self._isInitialized = True        

    def getDeviceSize(self):
        if not self._isInitialized:
            return (0,0)
        return (0,0)

    def writeText(self,text):
        if not self._isInitialized:
            return

    def connectDevice(self):
        pass

    def enterScreen(self, screen):
        if not self._isInitialized:
            return

    def leveScreen(self):
        if not self._isInitialized:
            return

    def shutdown(self):
        if not self._isInitialized:
            return
        self.leveScreen()
        self._isInitialized = False            

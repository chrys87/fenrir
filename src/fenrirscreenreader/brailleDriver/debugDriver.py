#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.brailleDriver import brailleDriver

class driver(brailleDriver):
    def __init__(self):
        brailleDriver.__init__(self)

    def initialize(self, environment):
        self.env = environment
        self._isInitialized = True
        self.deviceSize = (40,0)
        print('Braille Debug Driver: Initialized')

    def getDeviceSize(self):
        if not self._isInitialized:
            return (0,0)
        print('Braille Debug Driver: getDeviceSize ' + str(self.deviceSize))
        return self.deviceSize

    def writeText(self,text):
        if not self._isInitialized:
            return
        print('Braille Debug Driver: writeText:' + str(text))
        print('Braille Debug Driver: -----------------------------------')

    def connectDevice(self): 
        print('Braille Debug Driver: connectDevice')

    def enterScreen(self, screen):
        if not self._isInitialized:
            return
        print('Braille Debug Driver: enterScreen')

    def leveScreen(self):
        if not self._isInitialized:
            return
        print('Braille Debug Driver: leveScreen')

    def shutdown(self):
        if self._isInitialized:
            self.leveScreen()    
        self._isInitialized = False        
        print('Braille Debug Driver: Shutdown')

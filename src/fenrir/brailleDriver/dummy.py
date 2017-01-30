#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class driver():
    def __init__(self):
        self._isInitialized = False
    def initialize(self, environment):
        self.env = environment
        self._isInitialized = True

    def getDeviceSize(self):
        if not self._isInitialized:
            return (0,0)
        return (20,0)
   
    def writeText(self,text):
        if not self._isInitialized:
            return
        print(text)
    def connectDevice(self):
        pirnt('Connect Dummy Device')
        
    def enterScreen(self, screen):
        if not self._isInitialized:
            return
        pirnt('enter screen')

    def leveScreen(self):
        if not self._isInitialized:
            return
        pirnt('leve screen')

    def shutdown(self):
        if not self._isInitialized:
            return
        pirnt('shutdown')

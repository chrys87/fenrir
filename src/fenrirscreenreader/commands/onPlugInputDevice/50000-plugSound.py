#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import time

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.lastTime = time.time()
        self.tempDisable = False
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No description found'
    def run(self):
        playSound = False
        deviceList = self.env['runtime']['inputManager'].getLastDetectedDevices()
        try:
            for deviceEntry in deviceList:
            # dont play sounds for virtual devices
                playSound = playSound or not deviceEntry['virtual']
        except:
            playSound = True
        if playSound:
            if time.time() - self.lastTime > 5:
                self.env['runtime']['outputManager'].playSoundIcon(soundIcon = 'accept', interrupt=True)
                lastTime = time.time()
    def setCallback(self, callback):
        pass

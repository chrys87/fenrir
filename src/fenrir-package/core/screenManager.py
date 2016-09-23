#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import time

class screenManager():
    def __init__(self):
        self.autoIgnoreScreens = []

    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('screen', 'driver'), 'screenDriver')    
        if self.env['runtime']['settingsManager'].getSettingAsBool('screen', 'autodetectSuspendingScreen'):
            self.autoIgnoreScreens = self.env['runtime']['screenDriver'].getIgnoreScreens()
        
    def shutdown(self):
        self.env['runtime']['settingsManager'].shutdownDriver('screenDriver')

    def update(self):
        if not self.isSuspendingScreen():
            self.env['runtime']['screenDriver'].update()
            self.env['screenData']['lastScreenUpdate'] = time.time()

    def isSuspendingScreen(self):
        currScreen = self.env['runtime']['screenDriver'].getCurrScreen()
        return ((currScreen in \
          self.env['runtime']['settingsManager'].getSetting('screen', 'suspendingScreen').split(',')) or
          (currScreen in self.autoIgnoreScreens))
    def isScreenChange(self):
        return self.environment['screenData']['newTTY'] != self.environment['screenData']['oldTTY']

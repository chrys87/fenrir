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
        return self.env['screenData']['newTTY'] != self.env['screenData']['oldTTY']
    def getWindowAreaInText(self, text):
        if not self.env['runtime']['cursorManager'].isApplicationWindowSet():
            return text
        currApp = self.env['runtime']['applicationManager'].getCurrentApplication()
        windowText = ''
        windowList = text.split('\n')
        windowList = windowList[self.env['commandBuffer']['windowArea'][currApp]['1']['y']:self.env['commandBuffer']['windowArea'][currApp]['2']['y'] + 1]
        for line in windowList:
            windowText += line[self.env['commandBuffer']['windowArea'][currApp]['1']['x']:self.env['commandBuffer']['windowArea'][currApp]['2']['x'] + 1] + '\n'
        return windowText


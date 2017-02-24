#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import time

class screenManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('screen', 'driver'), 'screenDriver')    
        self.env['runtime']['screenDriver'].getCurrScreen()
        self.env['runtime']['screenDriver'].getSessionInformation()
        
    def shutdown(self):
        self.env['runtime']['settingsManager'].shutdownDriver('screenDriver')

    def update(self, trigger='onUpdate'):
        self.env['runtime']['screenDriver'].getCurrScreen()
        self.env['runtime']['screenDriver'].getSessionInformation()
        self.env['screenData']['oldApplication'] = self.env['screenData']['newApplication']            
        if self.isScreenChange():                 
            self.changeBrailleScreen()                                          
        if not self.isSuspendingScreen(self.env['screenData']['newTTY']):       
            self.env['runtime']['screenDriver'].update(trigger)
            if trigger == 'onUpdate' or self.isScreenChange() \
              or len(self.env['screenData']['newDelta']) > 6:
                self.env['runtime']['screenDriver'].getCurrApplication() 
            self.env['screenData']['lastScreenUpdate'] = time.time()

    def isSuspendingScreen(self, screen = None):
        if screen == None:
            screen = self.env['screenData']['newTTY']
        ignoreScreens = []
        fixIgnoreScreens = self.env['runtime']['settingsManager'].getSetting('screen', 'suspendingScreen')
        if fixIgnoreScreens != '':
            ignoreScreens.append(fixIgnoreScreens.split(',')) 
        if self.env['runtime']['settingsManager'].getSettingAsBool('screen', 'autodetectSuspendingScreen'):
            ignoreScreens.extend(self.env['screenData']['autoIgnoreScreens'])        
        return (screen in ignoreScreens)
 
    def isScreenChange(self):
        if not self.env['screenData']['oldTTY']:
            return False
        return self.env['screenData']['newTTY'] != self.env['screenData']['oldTTY']
    def isDelta(self):    
        return self.env['screenData']['newDelta'] != ''
    def isNegativeDelta(self):    
        return self.env['screenData']['newNegativeDelta'] != ''
    def getWindowAreaInText(self, text):
        if not self.env['runtime']['cursorManager'].isApplicationWindowSet():
            return text
        windowText = ''
        windowList = text.split('\n')
        currApp = self.env['runtime']['applicationManager'].getCurrentApplication()
        windowList = windowList[self.env['commandBuffer']['windowArea'][currApp]['1']['y']:self.env['commandBuffer']['windowArea'][currApp]['2']['y'] + 1]
        for line in windowList:
            windowText += line[self.env['commandBuffer']['windowArea'][currApp]['1']['x']:self.env['commandBuffer']['windowArea'][currApp]['2']['x'] + 1] + '\n'
        return windowText
    
    def injectTextToScreen(self, text, screen = None):
        try:
            self.env['runtime']['screenDriver'].injectTextToScreen(text, screen) 
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('screenManager:injectTextToScreen ' + str(e),debug.debugLevel.ERROR) 
            
    def changeBrailleScreen(self):
        if not self.env['runtime']['brailleDriver']:
            return
        if self.env['screenData']['oldTTY']:
            if not self.isSuspendingScreen(self.env['screenData']['oldTTY']):
                try:
                    self.env['runtime']['brailleDriver'].leveScreen() 
                except Exception as e:
                    self.env['runtime']['debug'].writeDebugOut('screenManager:changeBrailleScreen:leveScreen ' + str(e),debug.debugLevel.ERROR) 
        if not self.isSuspendingScreen():
            try:
                self.env['runtime']['brailleDriver'].enterScreen(self.env['screenData']['newTTY'])      
            except Exception as e:                
                self.env['runtime']['debug'].writeDebugOut('screenManager:changeBrailleScreen:enterScreen ' + str(e),debug.debugLevel.ERROR) 

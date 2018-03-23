#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import time, os

class screenManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('screen', 'driver'), 'screenDriver')    
        self.env['runtime']['screenDriver'].getCurrScreen()
        self.env['runtime']['screenDriver'].getCurrScreen()        
        self.env['runtime']['screenDriver'].getSessionInformation()
        
    def shutdown(self):
        self.env['runtime']['settingsManager'].shutdownDriver('screenDriver')
    def hanldeScreenChange(self, eventData):
        self.env['runtime']['screenDriver'].getCurrScreen()
        self.env['runtime']['screenDriver'].getSessionInformation()
        if self.isScreenChange():                 
            self.changeBrailleScreen()              
        if not self.isSuspendingScreen(self.env['screen']['newTTY']):       
            self.env['runtime']['screenDriver'].update(eventData, 'onScreenChange')
            self.env['screen']['lastScreenUpdate'] = time.time()            
    def handleScreenUpdate(self, eventData):
        self.env['screen']['oldApplication'] = self.env['screen']['newApplication']                                                    
        if not self.isSuspendingScreen(self.env['screen']['newTTY']):       
            self.env['runtime']['screenDriver'].update(eventData, 'onScreenUpdate')
            #if trigger == 'onUpdate' or self.isScreenChange() \
            #  or len(self.env['screen']['newDelta']) > 6:
            #    self.env['runtime']['screenDriver'].getCurrApplication() 
            self.env['screen']['lastScreenUpdate'] = time.time()
    def formatAttributes(self, attribute, attributeFormatString = None):
        if not attributeFormatString:
            attributeFormatString = self.env['runtime']['settingsManager'].getSetting('general', 'attributeFormatString')
        if not attributeFormatString:
            return ''
        if attributeFormatString == '':
            return ''
        attributeFormatString = attributeFormatString.replace('fenrirBGColor', self.env['runtime']['screenDriver'].getFenrirBGColor(attribute))
        attributeFormatString = attributeFormatString.replace('fenrirFGColor', self.env['runtime']['screenDriver'].getFenrirFGColor(attribute))
        attributeFormatString = attributeFormatString.replace('fenrirUnderline', self.env['runtime']['screenDriver'].getFenrirUnderline(attribute))
        attributeFormatString = attributeFormatString.replace('fenrirBold', self.env['runtime']['screenDriver'].getFenrirBold(attribute))
        attributeFormatString = attributeFormatString.replace('fenrirBlink', self.env['runtime']['screenDriver'].getFenrirBlink(attribute))
        attributeFormatString = attributeFormatString.replace('fenrirFontSize', self.env['runtime']['screenDriver'].getFenrirFontSize(attribute))                        
        attributeFormatString = attributeFormatString.replace('fenrirFont', self.env['runtime']['screenDriver'].getFenrirFont(attribute))        
        return attributeFormatString
    def isSuspendingScreen(self, screen = None):
        if screen == None:
            screen = self.env['screen']['newTTY']
        ignoreScreens = []
        fixIgnoreScreens = self.env['runtime']['settingsManager'].getSetting('screen', 'suspendingScreen')
        if fixIgnoreScreens != '':
            ignoreScreens.extend(fixIgnoreScreens.split(',')) 
        if self.env['runtime']['settingsManager'].getSettingAsBool('screen', 'autodetectSuspendingScreen'):
            ignoreScreens.extend(self.env['screen']['autoIgnoreScreens'])        
        self.env['runtime']['debug'].writeDebugOut('screenManager:isSuspendingScreen ' + str(ignoreScreens) + ' '+ str(self.env['screen']['newTTY']),debug.debugLevel.INFO) 
        try:
            ignoreFileName = self.env['runtime']['settingsManager'].getSetting('screen', 'suspendingScreenFile')
            if ignoreFileName != '':
                if os.access(ignoreFileName, os.R_OK):
                    with open(ignoreFileName) as fp:
                        ignoreScreens.extend(fp.read().replace('\n','').split(','))
        except:
            pass
        return (screen in ignoreScreens)
 
    def isScreenChange(self):
        if not self.env['screen']['oldTTY']:
            return False
        return self.env['screen']['newTTY'] != self.env['screen']['oldTTY']
    def isDelta(self, ignoreSpace=False):
        newDelta = self.env['screen']['newDelta']
        if ignoreSpace:
            newDelta = newDelta.strip()                
        return newDelta != ''
    def isNegativeDelta(self):    
        return self.env['screen']['newNegativeDelta'] != ''
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
        if not self.env['runtime']['settingsManager'].getSettingAsBool('braille', 'enabled'):
            return    
        if not self.env['runtime']['brailleDriver']:
            return
        if self.env['screen']['oldTTY']:
            if not self.isSuspendingScreen(self.env['screen']['oldTTY']):
                try:
                    self.env['runtime']['brailleDriver'].leveScreen() 
                except Exception as e:
                    self.env['runtime']['debug'].writeDebugOut('screenManager:changeBrailleScreen:leveScreen ' + str(e),debug.debugLevel.ERROR) 
        if not self.isSuspendingScreen():
            try:
                self.env['runtime']['brailleDriver'].enterScreen(self.env['screen']['newTTY'])      
            except Exception as e:                
                self.env['runtime']['debug'].writeDebugOut('screenManager:changeBrailleScreen:enterScreen ' + str(e),debug.debugLevel.ERROR) 

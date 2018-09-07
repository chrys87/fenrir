#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import screen_utils
import time, os, re, difflib

class screenManager():
    def __init__(self):
        self.differ = difflib.Differ()
        self.currScreenIgnored = False
        self.prevScreenIgnored = False
        self.prevScreenText = ''
        self.currScreenText = ''
        self.colums = None
        self.rows = None
    def getRows(self):
        return self.rows
    def getColumns(self):
        return self.colums
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('screen', 'driver'), 'screenDriver')    
        self.getCurrScreen()  
        self.getCurrScreen()
        self.getSessionInformation()        
        self.updateScreenIgnored()
        self.updateScreenIgnored()      
    def resetScreenText(self, screenText):
        self.prevScreenText = ''
        self.currScreenText = screenText          
    def setScreenText(self, screenText):
        self.prevScreenText = self.currScreenText
        self.currScreenText = screenText
    def getScreenText(self):
        return self.currScreenText
    def getCurrScreen(self):
        try:
            self.env['runtime']['screenDriver'].getCurrScreen()
        except:
            pass
    def getSessionInformation(self):
        try:    
            self.env['runtime']['screenDriver'].getSessionInformation()
        except:
            pass        
            
    def shutdown(self):
        self.env['runtime']['settingsManager'].shutdownDriver('screenDriver')
    def isCurrScreenIgnoredChanged(self):
        return self.getCurrScreenIgnored() != self.getPrevScreenIgnored()
    def hanldeScreenChange(self, eventData):
        self.getCurrScreen()
        self.getSessionInformation()        
        self.updateScreenIgnored()         
        if self.isCurrScreenIgnoredChanged():
            self.env['runtime']['inputManager'].setExecuteDeviceGrab()
        self.env['runtime']['inputManager'].handleDeviceGrab()        
              
        if self.isScreenChange():                 
            self.changeBrailleScreen() 

        if not self.isSuspendingScreen(self.env['screen']['newTTY']):       
            self.update(eventData, 'onScreenChange')
            self.env['screen']['lastScreenUpdate'] = time.time()
        else:
            self.env['runtime']['outputManager'].interruptOutput()        
                 
    def handleScreenUpdate(self, eventData):
        self.env['screen']['oldApplication'] = self.env['screen']['newApplication'] 
        self.updateScreenIgnored() 
        if self.isCurrScreenIgnoredChanged():
            self.env['runtime']['inputManager'].setExecuteDeviceGrab()
        self.env['runtime']['inputManager'].handleDeviceGrab()     
        if not self.getCurrScreenIgnored():       
            self.update(eventData, 'onScreenUpdate')
            #if trigger == 'onUpdate' or self.isScreenChange() \
            #  or len(self.env['screen']['newDelta']) > 6:
            #    self.env['runtime']['screenDriver'].getCurrApplication() 
            self.env['screen']['lastScreenUpdate'] = time.time()
        elif self.isCurrScreenIgnoredChanged():        
            self.env['runtime']['outputManager'].interruptOutput()              
    def getCurrScreenIgnored(self):
        return self.currScreenIgnored
    def getPrevScreenIgnored(self):
        return self.prevScreenIgnored      
    def updateScreenIgnored(self):
        self.prevScreenIgnored = self.currScreenIgnored              
        self.currScreenIgnored = self.isSuspendingScreen(self.env['screen']['newTTY'])                            
    def update(self, eventData, trigger='onUpdate'):
        # set new "old" values
        self.env['screen']['oldContentBytes'] = self.env['screen']['newContentBytes']
        self.env['screen']['oldContentText'] = self.env['screen']['newContentText']
        self.env['screen']['oldCursor'] = self.env['screen']['newCursor'].copy()   
        self.env['screen']['oldDelta'] = self.env['screen']['newDelta']
        self.env['screen']['oldNegativeDelta'] = self.env['screen']['newNegativeDelta']
        self.env['screen']['newContentBytes'] = eventData['bytes']

        # get metadata like cursor or screensize
        self.env['screen']['lines'] = int( eventData['lines'])
        self.env['screen']['columns'] = int( eventData['columns'])
        self.colums = int( eventData['columns'])
        self.rows = int( eventData['lines'])        
        self.env['screen']['newCursor']['x'] = int( eventData['textCursor']['x'])
        self.env['screen']['newCursor']['y'] = int( eventData['textCursor']['y'])
        self.env['screen']['newTTY'] = eventData['screen']
        self.env['screen']['newContentText'] = eventData['text']

        # screen change
        if self.isScreenChange():
            self.env['screen']['oldContentBytes'] = b''
            self.resetScreenText(eventData['text'])            
            self.env['runtime']['attributeManager'].resetAttributes(eventData['attributes'])
            self.env['runtime']['attributeManager'].resetAttributeCursor()            
            self.env['screen']['oldContentText'] = ''
            self.env['screen']['oldCursor']['x'] = 0
            self.env['screen']['oldCursor']['y'] = 0
            self.env['screen']['oldDelta'] = ''          
            self.env['screen']['oldNegativeDelta'] = '' 
        else:
            self.setScreenText(eventData['text'])        
            self.env['runtime']['attributeManager'].setAttributes(eventData['attributes'])
        # initialize current deltas
        self.env['screen']['newNegativeDelta'] = ''
        self.env['screen']['newDelta'] = ''
        self.env['runtime']['attributeManager'].resetAttributeDelta()

        # changes on the screen
        oldScreenText = re.sub(' +',' ',self.env['runtime']['screenManager'].getWindowAreaInText(self.env['screen']['oldContentText']))
        newScreenText = re.sub(' +',' ',self.env['runtime']['screenManager'].getWindowAreaInText(self.env['screen']['newContentText']))        
        typing = False
        diffList = []        
        
        if (self.env['screen']['oldContentText'] != self.env['screen']['newContentText']):
            if self.env['screen']['newContentText'] != '' and self.env['screen']['oldContentText'] == '':
                if oldScreenText == '' and\
                  newScreenText != '':
                    self.env['screen']['newDelta'] = newScreenText
            else:
                cursorLineStart = self.env['screen']['newCursor']['y'] * self.env['screen']['columns'] + self.env['screen']['newCursor']['y']
                cursorLineEnd = cursorLineStart  + self.env['screen']['columns']         
                if abs(self.env['screen']['oldCursor']['x'] - self.env['screen']['newCursor']['x']) >= 1 and \
                  self.env['screen']['oldCursor']['y'] == self.env['screen']['newCursor']['y'] and \
                  self.env['screen']['newContentText'][:cursorLineStart] == self.env['screen']['oldContentText'][:cursorLineStart] and \
                  self.env['screen']['newContentText'][cursorLineEnd:] == self.env['screen']['oldContentText'][cursorLineEnd:]:
                    cursorLineStartOffset = cursorLineStart
                    cursorLineEndOffset = cursorLineEnd
                    #if cursorLineStart < cursorLineStart + self.env['screen']['newCursor']['x'] - 4:
                    #    cursorLineStartOffset = cursorLineStart + self.env['screen']['newCursor']['x'] - 4
                    if cursorLineEnd > cursorLineStart + self.env['screen']['newCursor']['x'] + 3:
                        cursorLineEndOffset = cursorLineStart + self.env['screen']['newCursor']['x'] + 3                                               
                    oldScreenText = self.env['screen']['oldContentText'][cursorLineStartOffset:cursorLineEndOffset] 
                    # oldScreenText = re.sub(' +',' ',oldScreenText)
                    newScreenText = self.env['screen']['newContentText'][cursorLineStartOffset:cursorLineEndOffset]
                    #newScreenText = re.sub(' +',' ',newScreenText)
                    diff = self.differ.compare(oldScreenText, newScreenText) 
                    diffList = list(diff)
                    typing = True                    
                    tempNewDelta = ''.join(x[2:] for x in diffList if x[0] == '+')
                    if tempNewDelta.strip() != '':
                        if tempNewDelta != ''.join(newScreenText[self.env['screen']['oldCursor']['x']:self.env['screen']['newCursor']['x']].rstrip()):
                            diffList = ['+ ' + self.env['screen']['newContentText'].split('\n')[self.env['screen']['newCursor']['y']] +'\n']
                            typing = False
                else:
                    diff = self.differ.compare(oldScreenText.split('\n'),\
                      newScreenText.split('\n'))                    
                    diffList = list(diff)

                if not typing:
                    self.env['screen']['newDelta'] = '\n'.join(x[2:] for x in diffList if x[0] == '+')
                else:
                    self.env['screen']['newDelta'] = ''.join(x[2:] for x in diffList if x[0] == '+')             
                self.env['screen']['newNegativeDelta'] = ''.join(x[2:] for x in diffList if x[0] == '-')

        # track highlighted
        try:
            if self.env['runtime']['attributeManager'].isAttributeChange():
                if self.env['runtime']['settingsManager'].getSettingAsBool('focus', 'highlight'):
                    attributeDelta, attributeCursor = self.env['runtime']['attributeManager'].trackHighlights()
                    if attributeCursor:                    
                        self.env['runtime']['attributeManager'].setAttributeCursor(attributeCursor)
                        self.env['runtime']['attributeManager'].setAttributeDelta(attributeDelta)                    
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('screenManager:update:highlight: ' + str(e),debug.debugLevel.ERROR) 

    def isSuspendingScreen(self, screen = None):
        if screen == None:
            screen = self.env['screen']['newTTY']
        ignoreScreens = []
        fixIgnoreScreens = self.env['runtime']['settingsManager'].getSetting('screen', 'suspendingScreen')
        if fixIgnoreScreens != '':
            ignoreScreens.extend(fixIgnoreScreens.split(',')) 
        if self.env['runtime']['settingsManager'].getSettingAsBool('screen', 'autodetectSuspendingScreen'):
            ignoreScreens.extend(self.env['screen']['autoIgnoreScreens'])
        self.env['runtime']['debug'].writeDebugOut('screenManager:isSuspendingScreen ignore:' + str(ignoreScreens) + ' current:'+ str(screen ), debug.debugLevel.INFO)         
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

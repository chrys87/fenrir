#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, sys, signal, time

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

from core import settingsManager
from core import debug

class fenrir():
    def __init__(self):
        try:
            self.environment = settingsManager.settingsManager().initFenrirConfig()
            if not self.environment:
                raise RuntimeError('Cannot Initialize. Maybe the configfile is not available or not parseable')
        except RuntimeError:
            raise
        self.environment['runtime']['outputManager'].presentText("Start Fenrir", soundIcon='ScreenReaderOn', interrupt=True)          
        signal.signal(signal.SIGINT, self.captureSignal)
        signal.signal(signal.SIGTERM, self.captureSignal)
        self.wasCommand = False

    def proceed(self):
        while(self.environment['generalInformation']['running']):
            try:
                self.handleProcess()
            except Exception as e:
                print(e)
                self.environment['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR) 
        self.shutdown()

    def handleProcess(self):
        eventReceived = self.environment['runtime']['inputManager'].getInputEvent()
        startTime = time.time()
        if eventReceived:  
            self.prepareCommand()
            if not (self.wasCommand or self.environment['runtime']['inputManager'].isFenrirKeyPressed() or self.environment['generalInformation']['tutorialMode']):
                self.environment['runtime']['inputManager'].writeEventBuffer()
            if self.environment['runtime']['inputManager'].noKeyPressed():
                if self.wasCommand:
                        self.wasCommand = False   
                        self.environment['runtime']['inputManager'].clearEventBuffer()            
                if self.environment['generalInformation']['tutorialMode']:
                    self.environment['runtime']['inputManager'].clearEventBuffer()
                if self.environment['input']['keyForeward'] > 0:
                    self.environment['input']['keyForeward'] -=1
                self.environment['input']['prevDeepestInput'] = []                           
                self.environment['runtime']['screenManager'].update()
                            
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onInput')                
        else:
            self.environment['runtime']['screenManager'].update()

        if self.environment['runtime']['applicationManager'].isApplicationChange():
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onApplicationChange')
            self.environment['runtime']['commandManager'].executeSwitchTrigger('onSwitchApplicationProfile', \
              self.environment['runtime']['applicationManager'].getPrevApplication(), \
              self.environment['runtime']['applicationManager'].getCurrentApplication())            
        
        if self.environment['runtime']['screenManager'].isScreenChange():    
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onScreenChanged')             
        else:
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onScreenUpdate')         
            
        self.handleCommands()
        #print(time.time()-startTime)        

    def prepareCommand(self):
        if self.environment['input']['keyForeward'] > 0:
            return
        shortcut = self.environment['runtime']['inputManager'].getCurrShortcut()        
        #print(shortcut)
        command = self.environment['runtime']['inputManager'].getCommandForShortcut(shortcut)        
        self.environment['runtime']['commandManager'].queueCommand(command)  
        if len(self.environment['input']['prevDeepestInput']) < len(self.environment['input']['currInput']):
            self.wasCommand = command != ''
            self.environment['input']['prevDeepestInput'] = self.environment['input']['currInput'].copy()    
    
    def handleCommands(self):
        if time.time() - self.environment['commandInfo']['lastCommandExecutionTime'] < 0.2:
            return        
        if not self.environment['runtime']['commandManager'].isCommandQueued():
            return
        self.environment['runtime']['commandManager'].executeCommand( self.environment['commandInfo']['currCommand'], 'commands')

    def shutdownRequest(self):
        self.environment['generalInformation']['running'] = False

    def captureSignal(self, siginit, frame):
        self.shutdownRequest()

    def shutdown(self):
        if self.environment['runtime']['inputManager']:
            self.environment['runtime']['inputManager'].shutdown()                      
            del self.environment['runtime']['inputManager']
        self.environment['runtime']['outputManager'].presentText("Quit Fenrir", soundIcon='ScreenReaderOff', interrupt=True)   
        time.sleep(0.9) # wait a little for sound
        
        if self.environment['runtime']['screenManager']:
            self.environment['runtime']['screenManager'].shutdown()  
            del self.environment['runtime']['screenManager']
        if self.environment['runtime']['commandManager']:
            self.environment['runtime']['commandManager'].shutdown()                                    
            del self.environment['runtime']['commandManager']
        if self.environment['runtime']['outputManager']:
            self.environment['runtime']['outputManager'].shutdown()    
            del self.environment['runtime']['outputManager']
        if self.environment['runtime']['punctuationManager']:
            self.environment['runtime']['punctuationManager'].shutdown()    
            del self.environment['runtime']['punctuationManager']
        if self.environment['runtime']['cursorManager']:
            self.environment['runtime']['cursorManager'].shutdown()    
            del self.environment['runtime']['cursorManager']
        if self.environment['runtime']['applicationManager']:
            self.environment['runtime']['applicationManager'].shutdown()    
            del self.environment['runtime']['applicationManager']
            
        if self.environment['runtime']['debug']:
            self.environment['runtime']['debug'].shutdown() 
            del self.environment['runtime']['debug']
        time.sleep(0.2) # wait a little before splatter it :)
        self.environment = None

if __name__ == "__main__":
    app = fenrir()
    app.proceed()
    del app

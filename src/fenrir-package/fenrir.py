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
        if eventReceived:  
            self.prepareCommand()
            if not (self.environment['runtime']['inputManager'].isConsumeInput() or \
              self.environment['runtime']['inputManager'].isFenrirKeyPressed()) and \
              not self.environment['runtime']['commandManager'].isCommandQueued():
                self.environment['runtime']['inputManager'].writeEventBuffer()
            elif self.environment['runtime']['inputManager'].noKeyPressed():
                self.environment['runtime']['inputManager'].clearEventBuffer()

        try:
            self.environment['runtime']['screenManager'].update()
        except Exception as e:
            print(e)
            self.environment['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)         
        
        if self.environment['screenData']['newApplication'] != self.environment['screenData']['oldApplication']:
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onApplicationChange')
            self.environment['runtime']['commandManager'].executeSwitchTrigger(self, 'onSwitchApplicationProfile', \
              self.environment['screenData']['oldApplication'], self.environment['screenData']['newApplication'])            
        self.environment['runtime']['commandManager'].executeDefaultTrigger('onInput')
        if self.environment['screenData']['newTTY'] == self.environment['screenData']['oldTTY']:                 
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onScreenUpdate')         
        else:
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onScreenChanged')             
        self.handleCommands()

    def prepareCommand(self):
        if self.environment['input']['keyForeward']:
            return
        shortcut = self.environment['runtime']['inputManager'].getCurrShortcut()        
        command = self.environment['runtime']['inputManager'].getCommandForShortcut(shortcut)        
        self.environment['runtime']['commandManager'].queueCommand(command)           
    
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
        time.sleep(.3) # wait a little for sound
        
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
        if self.environment['runtime']['reviewManager']:
            self.environment['runtime']['reviewManager'].shutdown()    
            del self.environment['runtime']['reviewManager']

        if self.environment['runtime']['debug']:
            self.environment['runtime']['debug'].shutdown() 
            del self.environment['runtime']['debug']
        time.sleep(0.5) # wait a little before splatter it :)
        self.environment = None

if __name__ == "__main__":
    app = fenrir()
    app.proceed()
    del app

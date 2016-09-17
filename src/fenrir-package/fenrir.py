#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, sys, signal, time

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

from core import settingsManager
from utils import debug

class fenrir():
    def __init__(self):
        try:
            self.environment = settingsManager.settingsManager().initFenrirConfig()
            if not self.environment:
                raise RuntimeError('Cannot Initialize. Maybe the configfile is not available or not parseable')
        except RuntimeError:
            raise
        signal.signal(signal.SIGINT, self.captureSignal)
    
    def proceed(self):
        self.environment['runtime']['outputManager'].presentText(self.environment, "Start Fenrir", soundIcon='ScreenReaderOn', interrupt=True)          
        while(self.environment['generalInformation']['running']):
            try:
                self.handleProcess()
            except Exception as e:
                print(e)
                self.environment['runtime']['debug'].writeDebugOut(self.environment,str(e),debug.debugLevel.ERROR) 
        self.shutdown()

    def handleProcess(self):
        timeout = self.environment['runtime']['inputManager'].proceedInputEvent(self.environment)
        try:
            self.environment['runtime']['screenManager'].update(self.environment)
        except Exception as e:
            print(e)
            self.environment['runtime']['debug'].writeDebugOut(self.environment, str(e),debug.debugLevel.ERROR)                
        if not timeout:  
            self.prepareCommand()
            self.environment['runtime']['commandManager'].executeTriggerCommands(self.environment, 'onInput')            
        self.environment['runtime']['commandManager'].executeTriggerCommands(self.environment, 'onScreenChanged')        
        self.handleCommands()

    def prepareCommand(self):
        if self.environment['input']['keyForeward']:
            return
        shortcut = self.environment['runtime']['inputManager'].getCurrShortcut(self.environment)        
        command = self.environment['runtime']['inputManager'].getCommandForShortcut(self.environment, shortcut)        
        print(command)
        self.environment['runtime']['commandManager'].queueCommand(self.environment, command)           
    
    def handleCommands(self):
        if self.environment['input']['keyForeward']:
            return
        if self.environment['runtime']['commandManager'].isCommandQueued(self.environment):
            self.environment['runtime']['commandManager'].executeCommand(self.environment, self.environment['commandInfo']['currCommand'], 'commands')

    def shutdownRequest(self):
        self.environment['generalInformation']['running'] = False

    def captureSignal(self, siginit, frame):
        self.shutdownRequest()

    def shutdown(self):
        if self.environment['runtime']['inputManager']:
            self.environment['runtime']['inputManager'].shutdown(self.environment)                      
        self.environment['runtime']['outputManager'].presentText(self.environment, "Quit Fenrir", soundIcon='ScreenReaderOff', interrupt=True)   
        time.sleep(1.0) # wait a little before splatter it :)
        
        if self.environment['runtime']['screenManager']:
            self.environment['runtime']['screenManager'].shutdown(self.environment)  
        if self.environment['runtime']['commandManager']:
            self.environment['runtime']['commandManager'].shutdown(self.environment)                                    
        if self.environment['runtime']['outputManager']:
            self.environment['runtime']['outputManager'].shutdown(self.environment)                                      
      
        if self.environment['runtime']['debug']:
            self.environment['runtime']['debug'].closeDebugFile()                   
        time.sleep(0.8) # wait a little before splatter it :)
        self.environment = None

if __name__ == "__main__":
    app = fenrir()
    app.proceed()

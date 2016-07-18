#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, sys, time, signal

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

from threading import Thread
from core import environment 
from core import settingsManager

class fenrir():
    def __init__(self):
        self.threadonInput = Thread(target=self.onInput, args=())
        
        self.environment = settingsManager.settingsManager().initFenrirConfig()
        signal.signal(signal.SIGINT, self.captureSignal)
    
    def proceed(self):
        #self.threadonInput.start()
        #while(self.environment['generalInformation']['running']):
        self.onInput()
        self.shutdown()

    def onInput(self):
        while(self.environment['generalInformation']['running']):
            self.environment, timeout = self.environment['runtime']['inputManager'].getKeyPressed(self.environment)
            self.environment = self.environment['runtime']['commandManager'].getCommandForShortcut(self.environment)
            self.environment = self.environment['runtime']['screenDriver'].analyzeScreen(self.environment, 'onInput')
            if not timeout:
                self.environment = self.environment['runtime']['commandManager'].executeTriggerCommands(self.environment, 'onInput')
            self.environment = self.environment['runtime']['commandManager'].executeTriggerCommands(self.environment, 'onScreenChanged') 
            if self.environment['commandInfo']['currCommand'] != '':
                self.environment['input']['currShortcut'] = {}
                self.environment['input']['currShortcutString'] = ''
                self.handleCommands()
            self.environment['runtime']['globalLock'].release()

    def updateScreen(self):
            return
            self.environment['runtime']['globalLock'].acquire(True)
            self.environment = self.environment['runtime']['screenDriver'].analyzeScreen(self.environment,'updateScreen')
            self.environment = self.environment['runtime']['commandManager'].executeTriggerCommands(self.environment, 'onScreenChanged')            
            self.environment['runtime']['globalLock'].release()
            time.sleep(0.5)

    def handleCommands(self):
        if (self.environment['commandInfo']['currCommand'] != ''):# and \
#          (time.time() - self.environment['commandInfo']['lastCommandTime'] >= 0.01):
            self.environment = self.environment['runtime']['commandManager'].executeCommand(self.environment, self.environment['commandInfo']['currCommand'], 'commands')

    def shutdown(self):
        self.environment['generalInformation']['running'] = False
        if self.environment['runtime']['speechDriver'] != None:
            self.environment['runtime']['speechDriver'].shutdown()
        if self.environment['runtime']['debug'] != None:
            self.environment['runtime']['debug'].closeDebugFile()
        if self.environment['runtime']['soundDriver'] != None:
            self.environment['runtime']['soundDriver'].shutdown()

    def captureSignal(self, siginit, frame):
        self.shutdown()

app = fenrir()
app.proceed()

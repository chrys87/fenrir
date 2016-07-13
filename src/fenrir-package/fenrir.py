#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, sys, time, signal

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

from threading import Thread
from core import environment 
from core import inputManager
from core import commandManager
from core import settingsManager
from utils import debug

class fenrir():
    def __init__(self):
        self.threadHandleInput = None
        self.environment = environment.environment
        self.environment['runtime']['inputManager'] = inputManager.inputManager()
        self.environment['runtime']['settingsManager'] = settingsManager.settingsManager()
        self.environment = self.environment['runtime']['settingsManager'].loadShortcuts(self.environment)
        self.environment = self.environment['runtime']['settingsManager'].loadSettings(self.environment)

        self.environment['runtime']['commandManager'] = commandManager.commandManager()
        self.environment = self.environment['runtime']['commandManager'].loadCommands(self.environment,'commands')
        self.environment = self.environment['runtime']['commandManager'].loadCommands(self.environment,'onInput')
        self.environment = self.environment['runtime']['commandManager'].loadCommands(self.environment,'onScreenChanged')
        self.environment['runtime']['debug'] = debug.debug()
        signal.signal(signal.SIGINT, self.captureSignal)
        self.environment = self.environment['runtime']['settingsManager'].loadSpeechDriver(self.environment,\
          self.environment['runtime']['settingsManager'].getSetting(self.environment,'speech', 'driver'))
        self.environment = self.environment['runtime']['settingsManager'].loadScreenDriver(self.environment,\
          self.environment['runtime']['settingsManager'].getSetting(self.environment,'screen', 'driver'))
        self.environment = self.environment['runtime']['settingsManager'].loadSoundDriver(self.environment,\
          self.environment['runtime']['settingsManager'].getSetting(self.environment,'sound', 'driver'))   
     
    def proceed(self):
        self.threadHandleInput = Thread(target=self.handleInput, args=())
        self.threadHandleInput.start()
        self.updateScreen()
        while(self.environment['generalInformation']['running']):
            self.updateScreen()
        self.shutdown()

    def handleInput(self):
        while(self.environment['generalInformation']['running']):
            self.environment = self.environment['runtime']['inputManager'].getKeyPressed(self.environment)
            self.environment = self.environment['runtime']['commandManager'].getCommandForShortcut(self.environment)
            self.environment = self.environment['runtime']['screenDriver'].analyzeScreen(self.environment)
            self.environment = self.environment['runtime']['commandManager'].executeTriggerCommands(self.environment, 'onInput')
            if self.environment['input']['currShortcutString'] != '':
                self.handleCommands()

    def updateScreen(self):
            self.environment = self.environment['runtime']['screenDriver'].analyzeScreen(self.environment)
            self.environment = self.environment['runtime']['commandManager'].executeTriggerCommands(self.environment, 'onScreenChanged')            
            time.sleep(0.5)

    def handleCommands(self):
        if (self.environment['commandInfo']['currCommand'] != '') and \
          (time.time() - self.environment['commandInfo']['lastCommandTime'] >= 0.04):
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

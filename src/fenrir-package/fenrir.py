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

from speech import espeak as es
from speech import speechd as sd
from screen import linux as lx

class fenrir():
    def __init__(self):
        self.threadUpdateScreen = None
        self.threadHandleInput = None
        self.threadHandleCommandQueue = None
        self.environment = environment.environment
        self.environment['runtime']['inputManager'] = inputManager.inputManager()
        self.environment['runtime']['settingsManager'] = settingsManager.settingsManager()
        self.environment = self.environment['runtime']['settingsManager'].loadShortcuts(self.environment)
        self.environment['runtime']['commandManager'] = commandManager.commandManager()
        self.environment = self.environment['runtime']['commandManager'].loadCommands(self.environment,'commands')
        self.environment = self.environment['runtime']['commandManager'].loadCommands(self.environment,'onInput')
        self.environment = self.environment['runtime']['commandManager'].loadCommands(self.environment,'onScreenChanged')
        self.environment['runtime']['debug'] = debug.debug()
        signal.signal(signal.SIGINT, self.captureSignal)
        # the following hard coded, in future we have a config loader
        self.environment['runtime']['speechDriver'] = sd.speech()
        self.environment['runtime']['screenDriver'] = lx.screenManager()

    def proceed(self):
        self.threadUpdateScreen = Thread(target=self.updateScreen, args=())
        self.threadHandleInput = Thread(target=self.handleInput, args=())
        self.threadCommands = Thread(target=self.handleCommands, args=())
        self.threadUpdateScreen.start()
        self.threadHandleInput.start()
        #self.threadCommands.start()
        while(self.environment['generalInformation']['running']):
            #starttime = time.time()
            time.sleep(1)
            #self.updateScreen()
            #self.handleInput()
            #self.handleCommands()
            #print(time.time() -starttime)
        self.shutdown()

    def handleInput(self):
        while(self.environment['generalInformation']['running']):
            self.environment = self.environment['runtime']['inputManager'].getKeyPressed(self.environment)
            self.environment = self.environment['runtime']['screenDriver'].analyzeScreen(self.environment)
            #print(self.environment['screenData']['delta'])
            if self.environment['input']['currShortcutString'] != '':
                self.handleCommands()
            print('läuft')
            #if self.environment['input']['currShortcutString'] == '':
            #    self.environment['commandInfo']['currCommand'] = ''

    def updateScreen(self):
        while(self.environment['generalInformation']['running']):
            self.environment = self.environment['runtime']['screenDriver'].analyzeScreen(self.environment)
            time.sleep(0.5)

    def handleCommands(self):
        #while(self.environment['generalInformation']['running']):
        self.environment = self.environment['runtime']['commandManager'].getCommandForShortcut(self.environment)
        #self.environment['input']['currShortcut'] = {} 
        print( self.environment['commandInfo']['currCommand'] )
        if (self.environment['commandInfo']['currCommand'] != '') and \
          (time.time() - self.environment['commandInfo']['lastCommandTime'] >= 0.4):
            self.environment = self.environment['runtime']['commandManager'].executeCommand(self.environment, self.environment['commandInfo']['currCommand'], 'commands')
            #time.sleep(0.5)

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

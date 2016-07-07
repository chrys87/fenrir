#!/bin/python

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, sys, time

DEBUG = False

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

from threading import Thread
from core import environment 
from core import inputManager
from utils import debug

from speech import espeak as es
from speech import speechd as sd
from screen import linux as lx

class fenrir():
    def __init__(self):
        self.threadUpdateScreen = None
        self.threadHandleInput = None
        self.runtime = environment.runtime
        self.runtime['inputManager'] = inputManager.inputManager()
        if DEBUG:
            self.runtime['debug'] = debug.debug()
        self.settings = environment.settings
        self.bindings = {}
        self.autospeak = []
        self.soundIcons = {}
        
        # the following hard coded, in future we have a config loader
        self.runtime['speechDriverString'] = 'speechd'
        self.runtime['speechDriver'] = sd.speech()
        self.runtime['screenDriverString'] = 'linux'
        self.runtime['screenDriver'] = lx.screenManager()

    def proceed(self):
        self.threadUpdateScreen = Thread(target=self.updateScreen, args=())
        self.threadHandleInput = Thread(target=self.handleInput, args=())
        self.threadUpdateScreen.start()
        self.threadHandleInput.start()
        while(self.runtime['running']):
            time.sleep(2)
        self.shutdown()

    def handleInput(self):
        while(self.runtime['running']):
            self.runtime = self.runtime['inputManager'].getKeyPressed(self.runtime)

    def updateScreen(self):
        while(self.runtime['running']):
            self.runtime = self.runtime['screenDriver'].analyzeScreen(self.runtime)

    def shutdown(self):
        self.threadUpdateScreen.stop()
        self.threadHandleInput.stop()

app = fenrir()
app.proceed()

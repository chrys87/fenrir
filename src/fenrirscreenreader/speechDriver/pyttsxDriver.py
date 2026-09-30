#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# Espeak driver

from threading import Thread, Lock
from fenrirscreenreader.core import debug
from fenrirscreenreader.core.speechDriver import speechDriver

class driver(speechDriver):
    def __init__(self):
        speechDriver.__init__(self)
        self._engine = None
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        if self._isInitialized:
            self.cancel()
            self._engine.endLoop()
        self._initialized = False
    def eventLoop(self):
        self._engine.startLoop()
    def startEngine(self):
        try:
            import pyttsx3
            if self.module != '':
                self._engine = pyttsx3.init(self.module)
            else:
                self._engine = pyttsx3.init()
            self.eventLoopThread = Thread(target=self.eventLoop)
            self._isInitialized = True
            self.eventLoopThread.start()
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('SpeechDriver:initialize:' + str(e),debug.debugLevel.ERROR)
    
    def speak(self,text, interrupt=True):
        if not self._isInitialized:
            self.startEngine()
            if not self._isInitialized:
                return
        if not interrupt:
            self.cancel()
        try:
            self._engine.setProperty('volume', self.volume) 
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('SpeechDriver:speak:volume:' + str(e),debug.debugLevel.ERROR) 
        try:
            self._engine.setProperty('rate', self.rate) 
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('SpeechDriver:speak:rate:' + str(e),debug.debugLevel.ERROR) 
        try:
            self._engine.setProperty('pitch', self.pitch)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('SpeechDriver:speak:pitch:' + str(e),debug.debugLevel.ERROR)
        if self.voice != None and self.voice != '':
            try:
                self._engine.setProperty('voice', self.voice) 
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('SpeechDriver:speak:voice:' + str(e),debug.debugLevel.ERROR)
        elif self.language != None and self.language != '':
            try:
                self._engine.setProperty('voice', self.language)
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('SpeechDriver:speak:language:' + str(e),debug.debugLevel.ERROR)
        self._engine.say(text)

    def cancel(self):
        if not self._isInitialized:
            return
        self._engine.stop()

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        self.pitch = pitch
        
    def setRate(self, rate):
        if not self._isInitialized:
            return
        self.rate = rate

    def setVoice(self, voice):
        if voice == '':
            return
        self.voice = str(voice)
        if self._isInitialized and self._engine:
            try:
                self._engine.setProperty('voice', self.voice)
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('pyttsxDriver:setVoice:' + str(e), debug.debugLevel.ERROR)

    def getVoices(self):
        if not self._isInitialized:
            self.startEngine()
        if not self._isInitialized or not self._engine:
            return []
        try:
            voices = []
            for v in self._engine.getProperty('voices'):
                if hasattr(v, 'id') and v.id:
                    voices.append(str(v.id))
                elif hasattr(v, 'name') and v.name:
                    voices.append(str(v.name))
                elif isinstance(v, str):
                    voices.append(v)
            return voices
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('pyttsxDriver getVoices:' + str(e), debug.debugLevel.ERROR)
            return []

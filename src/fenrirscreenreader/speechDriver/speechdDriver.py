#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# speech-dispatcher driver

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.speechDriver import speechDriver

class driver(speechDriver):
    def __init__(self):
        speechDriver.__init__(self)
        self._sd = None

    def initialize(self, environment):
        self.env = environment
        try:
            import speechd 
            self._sd =  speechd.SSIPClient('fenrir')
            self._punct = speechd.PunctuationMode()
            self._isInitialized = True
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver initialize:' + str(e),debug.debugLevel.ERROR)

    def shutdown(self):
        if not self._isInitialized:
            return
        self.cancel()
        try:
            self._sd.close()
        except:
            pass
        self._isInitialized = False

    def speak(self,text, queueable=True):
        if not queueable:
            self.cancel()
        if not self._isInitialized:
            if not queueable:
                self.cancel()
            self.initialize(self.env)
            if not self._isInitialized:
                return

        try:
            self._sd.set_output_module(self.module)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver setModule:' + str(e),debug.debugLevel.ERROR)

        try:
            if self.language != '':
                self._sd.set_language(self.language)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver set_language:' + str(e),debug.debugLevel.ERROR)

        try:
            if self.voice:
                if self.voice != '':
                    self._sd.set_synthesis_voice(self.voice)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver setVoice:' + str(e),debug.debugLevel.ERROR)

        try:
            self._sd.set_punctuation(self._punct.NONE)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver set_punctuation:' + str(e),debug.debugLevel.ERROR)

        try:
            self._sd.speak(text)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver speak:' + str(e),debug.debugLevel.ERROR)
            self._isInitialized = False

    def cancel(self):
        if not self._isInitialized:
            return
        try:
            self._sd.cancel()
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver cancel:' + str(e),debug.debugLevel.ERROR)
            self._isInitialized = False

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        try:
            self._sd.set_pitch(int(-100 + pitch * 200)) 
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver setPitch:' + str(e),debug.debugLevel.ERROR)

    def setRate(self, rate):
        if not self._isInitialized:
            return 
        try:
            self._sd.set_rate(int(-100 + rate * 200))
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver setRate:' + str(e),debug.debugLevel.ERROR)

    def setVolume(self, volume):
        if not self._isInitialized:
            return 
        try:
            self._sd.set_volume(int(-100 + volume * 200))
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver setVolume:' + str(e),debug.debugLevel.ERROR)

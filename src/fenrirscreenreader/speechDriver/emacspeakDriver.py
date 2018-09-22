#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# generic driver

import pexpect
import shlex
import time
from fenrirscreenreader.core import debug
from fenrirscreenreader.core.speechDriver import speechDriver

class driver(speechDriver):
    def __init__(self):
        speechDriver.__init__(self)
    def initialize(self, environment):
        self.env = environment        
        try:
            self.server = pexpect.spawn('tclsh ' + self.env['runtime']['settingsManager'].getSetting('speech', 'serverPath'))
            self._isInitialized = True            
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver:initialize:' + str(e),debug.debugLevel.ERROR)     

    def shutdown(self):
        if self.server:
            try:
                self.server.terminate()
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('speechDriver:shutdown:self.server.terminate():' + str(e),debug.debugLevel.ERROR)    

    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return
        if not queueable: 
            self.cancel()
        try:
            cleanText = text
            for c in '[]{}\\|_@#^*<>\"`~^':
                cleanText.replace(c,'')
            cleanText = shlex.split(cleanText)
            for idx, word in enumerate(cleanText):
                cleanText[idx] = word
            cleanText = ' '.join(cleanText)
            cleanText = 'tts_say \"' + cleanText +'\"'
            self.server.sendline(cleanText) 
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver:speak:self.server.sendline():' + str(e),debug.debugLevel.ERROR)            
    
    def cancel(self):
        if not self._isInitialized:
            return
        try:
            self.server.sendline('stop')
        except Exception as e:
            print(e)
            self.env['runtime']['debug'].writeDebugOut('speechDriver:cancel:self.server.sendline():' + str(e),debug.debugLevel.ERROR)   
    
    def setRate(self, rate):
        if not self._isInitialized:
            return
        try:
            self.server.sendline('tts_set_speech_rate ' + str(int(rate * 400)))
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver:setRate:self.server.sendline():' + str(e),debug.debugLevel.ERROR)  
    
    def setLanguage(self, language):
        if not self._isInitialized:
            return
        self.server.sendline('set_lang ' + language)

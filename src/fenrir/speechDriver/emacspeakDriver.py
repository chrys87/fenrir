#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# generic driver

from core import debug
from subprocess import Popen, PIPE
import pexpect
import sys

class driver():
    def __init__(self):
        pass
    def initialize(self, environment):
        self._isInitialized = False    
        self.env = environment        
        try:
            self.server = pexpect.spawnu('tclsh +' self.env['runtime']['settingsManager'].getSetting('speech', 'serverPath'))   
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver:initialize:' + str(e),debug.debugLevel.ERROR)                
        self._isInitialized = True
        
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
            self.server.sendline('tts_say ' + '\"' + text +'\"')   
            #print(text.replace('"', '\\\"'))      
            #self.server.sendline('tts_say ' + '\"' + text.replace('"', '\\\"') +'\"') 
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver:speak:self.server.sendline():' + str(e),debug.debugLevel.ERROR)            
    
    def cancel(self):
        if not self._isInitialized:
            return
        try:
            self.server.sendline('s')  
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver:cancel:self.server.sendline():' + str(e),debug.debugLevel.ERROR)   
    
    def setCallback(self, callback):
        pass

    def clear_buffer(self):
        if not self._isInitialized:
            return

    def setVoice(self, voice):
        if not self._isInitialized:
            return

    def setPitch(self, pitch):
        pass

    def setRate(self, rate):
        if not self._isInitialized:
            return
        try:
            self.server.sendline('tts_set_speech_rate' + str(int(rate * 500)))
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver:setRate:self.server.sendline():' + str(e),debug.debugLevel.ERROR)  
    
    def setModule(self, module):
        pass
    def setLanguage(self, language):
        if not self._isInitialized:
            return
        self.server.sendline('set_lang ' + language)
    def setVolume(self, volume):
        pass

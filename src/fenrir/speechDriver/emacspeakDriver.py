#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# generic driver

from core import debug
from subprocess import Popen, PIPE
import pexpect
import ptyprocess
import sys
import time
from core.speechDriver import speechDriver

class driver(speechDriver):
    def __init__(self):
        speechDriver.__init__(self)
    def initialize(self, environment):
        self.env = environment        
        try:
            self.server = ptyprocess.PtyProcessUnicode.spawn(['tclsh ', self.env['runtime']['settingsManager'].getSetting('speech', 'serverPath')])
            #self.server = pexpect.spawnu('tclsh ' + self.env['runtime']['settingsManager'].getSetting('speech', 'serverPath'))
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
            cleanText = text.replace('}', '\}')
            cleanText = cleanText.replace('{', '\{')  
            cleanText = cleanText.replace('*', '\*')                                  
            cleanText = cleanText.replace('"', '\"')                    
            cleanText = cleanText.replace('\n', ' ')            
            cleanText = cleanText.replace('[', '\[')
            #print(text.replace('"', '\\\"'))      
            self.server.write('tts_say ' + '"' + cleanText +'"\n')             
            #self.server.sendline('tts_say ' + '"' + cleanText +'"') 
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver:speak:self.server.sendline():' + str(e),debug.debugLevel.ERROR)            
    
    def cancel(self):
        if not self._isInitialized:
            return
        try:
            self.server.write('s\n')            
            #self.server.sendline('s')
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver:cancel:self.server.sendline():' + str(e),debug.debugLevel.ERROR)   
    
    def setRate(self, rate):
        if not self._isInitialized:
            return
        try:
            self.server.write('tts_set_speech_rate ' + str(int(rate * 400)) + '\n')            
            #self.server.sendline('tts_set_speech_rate ' + str(int(rate * 400)) + '')
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('speechDriver:setRate:self.server.sendline():' + str(e),debug.debugLevel.ERROR)  
    
    def setLanguage(self, language):
        if not self._isInitialized:
            return
        self.server.write('set_lang ' + language + '\n')
        #self.server.sendline('set_lang ' + language + '')

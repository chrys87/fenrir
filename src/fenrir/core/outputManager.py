#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import string

class outputManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('speech', 'driver'), 'speechDriver')    
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('sound', 'driver'), 'soundDriver')    
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('braille', 'driver'), 'brailleDriver')      
    def shutdown(self):
        self.env['runtime']['settingsManager'].shutdownDriver('soundDriver')
        self.env['runtime']['settingsManager'].shutdownDriver('speechDriver')
        self.env['runtime']['settingsManager'].shutdownDriver('brailleDriver')
        
    def presentText(self, text, interrupt=True, soundIcon = '', ignorePunctuation=False, announceCapital=False):
        self.env['runtime']['debug'].writeDebugOut("presentText:\nsoundIcon:'"+soundIcon+"'\nText:\n" + text ,debug.debugLevel.INFO)
        if self.playSoundIcon(soundIcon, interrupt):
            self.env['runtime']['debug'].writeDebugOut("soundIcon found" ,debug.debugLevel.INFO)            
            return
        toAnnounceCapital = announceCapital and len(text.strip(' \n\t')) == 1 and text.strip(' \n\t').isupper()
        if toAnnounceCapital:
            if self.playSoundIcon('capital', False):
                toAnnounceCapital = False         

        self.speakText(text, interrupt, ignorePunctuation,toAnnounceCapital)
        self.brailleText(text, interrupt)

    def speakText(self, text, interrupt=True, ignorePunctuation=False, announceCapital=False):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'enabled'):
            self.env['runtime']['debug'].writeDebugOut("Speech disabled in outputManager.speakText",debug.debugLevel.INFO)
            return
        if self.env['runtime']['speechDriver'] == None:
            self.env['runtime']['debug'].writeDebugOut("No speechDriver in outputManager.speakText",debug.debugLevel.ERROR)
            return
        if interrupt:
            self.interruptOutput()
        try:
            self.env['runtime']['speechDriver'].setLanguage(self.env['runtime']['settingsManager'].getSetting('speech', 'language'))
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("setting speech language in outputManager.speakText",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)
        
        try:
            self.env['runtime']['speechDriver'].setVoice(self.env['runtime']['settingsManager'].getSetting('speech', 'voice'))
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("Error while setting speech voice in outputManager.speakText",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)        
        
        try:
            if announceCapital:
                self.env['runtime']['speechDriver'].setPitch(self.env['runtime']['settingsManager'].getSettingAsFloat('speech', 'capitalPitch'))            
            else:
                self.env['runtime']['speechDriver'].setPitch(self.env['runtime']['settingsManager'].getSettingAsFloat('speech', 'pitch'))
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("setting speech pitch in outputManager.speakText",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)            
        
        try:
            self.env['runtime']['speechDriver'].setRate(self.env['runtime']['settingsManager'].getSettingAsFloat('speech', 'rate'))
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("setting speech rate in outputManager.speakText",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)            
        
        try:
            self.env['runtime']['speechDriver'].setModule(self.env['runtime']['settingsManager'].getSetting('speech', 'module'))
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("setting speech module in outputManager.speakText",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)

        try:            
            self.env['runtime']['speechDriver'].setVolume(self.env['runtime']['settingsManager'].getSettingAsFloat('speech', 'volume'))
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("setting speech volume in outputManager.speakText ",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)            
        
        try:
            text = self.env['runtime']['punctuationManager'].proceedPunctuation(text,ignorePunctuation) 
            self.env['runtime']['speechDriver'].speak(text)
            self.env['runtime']['debug'].writeDebugOut("Speak: "+ text,debug.debugLevel.INFO)                
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("\"speak\" in outputManager.speakText ",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)            

    def brailleText(self, text, interrupt=True):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('braille', 'enabled'):
            return
        if self.env['runtime']['brailleDriver'] == None:
            return        
        self.env['runtime']['brailleDriver'].writeText(text)

    def interruptOutput(self):
        self.env['runtime']['speechDriver'].cancel()
        self.env['runtime']['debug'].writeDebugOut("Interrupt speech",debug.debugLevel.INFO)       
        

    def playSoundIcon(self, soundIcon = '', interrupt=True):
        if soundIcon == '':
            return False
        soundIcon = soundIcon.upper()
        if not self.env['runtime']['settingsManager'].getSettingAsBool('sound', 'enabled'):
            self.env['runtime']['debug'].writeDebugOut("Sound disabled in outputManager.speakText",debug.debugLevel.INFO)        
            return False  
            
        if self.env['runtime']['soundDriver'] == None:
            self.env['runtime']['debug'].writeDebugOut("No speechDriver in outputManager.speakText",debug.debugLevel.ERROR)        
            return False       
        try:
            self.env['runtime']['soundDriver'].setVolume(self.env['runtime']['settingsManager'].getSettingAsFloat('sound', 'volume'))
            self.env['runtime']['soundDriver'].playSoundFile(self.env['soundIcons'][soundIcon], interrupt)
            return True
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("\"playSoundIcon\" in outputManager.speakText ",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)            
        return False

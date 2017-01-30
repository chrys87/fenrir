#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import line_utils
import string, time

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
        
    def presentText(self, text, interrupt=True, soundIcon = '', ignorePunctuation=False, announceCapital=False, flush=False):
        if text == '':
            return
        self.env['runtime']['debug'].writeDebugOut("presentText:\nsoundIcon:'"+soundIcon+"'\nText:\n" + text ,debug.debugLevel.INFO)
        if self.playSoundIcon(soundIcon, interrupt):
            self.env['runtime']['debug'].writeDebugOut("soundIcon found" ,debug.debugLevel.INFO)            
            return
        if (len(text) > 1) and (text.strip(string.whitespace) == ''):
            return
        toAnnounceCapital = announceCapital and text[0].isupper()
        if toAnnounceCapital:
            if self.playSoundIcon('capital', False):
                toAnnounceCapital = False         

        self.speakText(text, interrupt, ignorePunctuation,toAnnounceCapital)
        if flush:
            self.brailleText(text, flush)

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
            text = text.replace('\n',' , ')

            self.env['runtime']['speechDriver'].speak(text)
            self.env['runtime']['debug'].writeDebugOut("Speak: "+ text,debug.debugLevel.INFO)                
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("\"speak\" in outputManager.speakText ",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)            

    def brailleText(self, text='', flush=False):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('braille', 'enabled'):
            return
        if self.env['runtime']['brailleDriver'] == None:
            return        
        size = self.env['runtime']['brailleDriver'].getDeviceSize()
        if flush:
            self.env['output']['nextFlush'] = time.time() + self.getFlushTime(text)
            self.env['output']['messageText'] = text
            self.env['runtime']['brailleDriver'].writeText('flush'+self.env['output']['messageText'] [self.env['output']['messageOffset']['x']: \
              self.env['output']['messageOffset']['x']+size[0]])         
        else:
            if self.env['output']['nextFlush'] < time.time():
                if self.env['output']['messageText'] != '':
                    self.env['output']['messageText'] = ''
                if self.env['output']['messageOffset'] != {'x':0,'y':0}:
                    self.env['output']['messageOffset'] = {'x':0,'y':0}
                cursor = self.env['runtime']['cursorManager'].getReviewOrTextCursor()
                x, y, currLine = \
                  line_utils.getCurrentLine(cursor['x'], cursor['y'], self.env['screenData']['newContentText'])                
                
                self.env['runtime']['brailleDriver'].writeText('notflush<>' + currLine +'<>'+currLine[cursor['x']:cursor['x'] + size[0]])
            else:
                self.env['runtime']['brailleDriver'].writeText('flush'+self.env['output']['messageText'] [self.env['output']['messageOffset']['x']: \
                  self.env['output']['messageOffset']['x']+size[0]])                          

    def interruptOutput(self):
        self.env['runtime']['speechDriver'].cancel()
        self.env['runtime']['debug'].writeDebugOut("Interrupt speech",debug.debugLevel.INFO)       

    def clearFlushTime(self):
        self.setFlushTime(0.0)

    def setFlushTime(self,newTime):
        self.env['output']['nextFlush'] = newTime

    def getFlushTime(self,text=''):
        if self.env['runtime']['settingsManager'].getSettingAsFloat('braille', 'flushTimeout') < 0 or \
          self.env['runtime']['settingsManager'].getSetting('braille', 'flushMode').upper() == 'NONE':
            return 999999999999    
        if self.env['runtime']['settingsManager'].getSetting('braille', 'flushMode').upper() == 'FIX':
            return self.env['runtime']['settingsManager'].getSettingAsFloat('braille', 'flushTimeout')
        if self.env['runtime']['settingsManager'].getSetting('braille', 'flushMode').upper() == 'CHAR':
            return self.env['runtime']['settingsManager'].getSettingAsFloat('braille', 'flushTimeout') * len(text)
        if self.env['runtime']['settingsManager'].getSetting('braille', 'flushMode').upper() == 'WORD':
            wordsList = text.split(' ')
            return self.env['runtime']['settingsManager'].getSettingAsFloat('braille', 'flushTimeout') * len( list( filter(None, wordsList) ) )
                           
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
    def announceActiveCursor(self, interrupt_p=False):        
        if self.env['runtime']['cursorManager'].isReviewMode():
            self.presentText(' review cursor ', interrupt=interrupt_p)                                
        else:
            self.presentText(' text cursor ', interrupt=interrupt_p)       
            

#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import line_utils
import string, time, re

class outputManager():
    def __init__(self):
        self.lastEcho = ''
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
        
    def presentText(self, text, interrupt=True, soundIcon = '', ignorePunctuation=False, announceCapital=False, flush=True, brailleAlternative = ''):
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
        self.lastEcho = text
        self.speakText(text, interrupt, ignorePunctuation,toAnnounceCapital)
        if flush:
            if brailleAlternative != '':
                brlText = brailleAlternative
            else:
                brlText = text
            self.brailleText(brlText, flush)
    def getLastEcho(self):
        return self.lastEcho
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
            if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'newLinePause'):        
                cleanText = text.replace('\n',' , ')
            else:
                cleanText = text.replace('\n',' ')

            cleanText = self.env['runtime']['textManager'].replaceHeadLines(cleanText)        
            cleanText = self.env['runtime']['punctuationManager'].proceedPunctuation(cleanText, ignorePunctuation) 
            cleanText = re.sub(' +$',' ', cleanText)            
            self.env['runtime']['speechDriver'].speak(cleanText)
            self.env['runtime']['debug'].writeDebugOut("Speak: "+ cleanText,debug.debugLevel.INFO)                
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("\"speak\" in outputManager.speakText ",debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)            

    def brailleText(self, text='', flush=True):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('braille', 'enabled'):
            return
        if self.env['runtime']['brailleDriver'] == None:
            return        
        if flush:
            self.env['output']['nextFlush'] = time.time() + self.getFlushTime(text)
            self.env['output']['messageOffset'] = {'x':0,'y':0}            
            self.env['output']['messageText'] = text
            displayText = self.getBrailleTextWithOffset(self.env['output']['messageText'], self.env['output']['messageOffset'])    
            self.env['runtime']['brailleDriver'].writeText('flush '+ displayText)         
        else:
            if self.env['output']['nextFlush'] < time.time():
                if self.env['output']['messageText'] != '':
                    self.env['output']['messageText'] = ''
                if self.env['output']['messageOffset'] != None:
                    self.env['output']['messageOffset'] = None
                cursor = self.getBrailleCursor()
                x, y, self.env['output']['brlText'] = \
                  line_utils.getCurrentLine(cursor['x'], cursor['y'], self.env['screen']['newContentText'])                
                displayText = self.getBrailleTextWithOffset(self.env['screen']['newContentText'], self.env['output']['cursorOffset'], cursor)    
                self.env['runtime']['brailleDriver'].writeText('notflush ' + displayText)                  
            else:
                displayText = self.getBrailleTextWithOffset(self.env['output']['messageText'], self.env['output']['messageOffset'])    
                self.env['runtime']['brailleDriver'].writeText('flush'+displayText)                          

    def getBrailleCursor(self):
        if self.env['runtime']['settingsManager'].getSetting('braille', 'cursorFollowMode').upper() == 'REVIEW':
            return self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        if self.env['runtime']['settingsManager'].getSetting('braille', 'cursorFollowMode').upper() == 'MANUAL':
            return self.env['runtime']['cursorManager'].getReviewOrTextCursor()            
        if self.env['runtime']['settingsManager'].getSetting('braille', 'cursorFollowMode').upper() == 'LAST':
            return self.env['runtime']['cursorManager'].getReviewOrTextCursor()
        return self.env['runtime']['cursorManager'].getReviewOrTextCursor()                     
    
    def getFixCursorCell(self):
        size = self.env['runtime']['brailleDriver'].getDeviceSize()[0]
        fixCell = self.env['runtime']['settingsManager'].getSettingAsInt('braille', 'fixCursorOnCell')
        if fixCell <= -1:
            return size[0]
        if fixCell >= size[0]:
            return size[0]
        return fixCell 
    def getActiveOffsetAndText(self):
        if self.env['output']['messageOffset']:
            return self.env['output']['messageOffset'], self.env['output']['messageText']
        if not self.env['output']['cursorOffset']:
            return self.getBrailleCursor(), self.env['screen']['newContentText']
        return self.env['output']['cursorOffset'], self.env['screen']['newContentText']
    def getHorizontalPanSize(self):
        size = self.env['runtime']['brailleDriver'].getDeviceSize()        
        if self.env['runtime']['settingsManager'].getSettingAsInt('braille', 'panSizeHorizontal') <= 0:
            return size[0]
        if self.env['runtime']['settingsManager'].getSettingAsInt('braille', 'panSizeHorizontal') >= size[0]:
            return size[0]            
        return self.env['runtime']['settingsManager'].getSettingAsInt('braille', 'panSizeHorizontal')
    def getHorizontalPanLevel(self,offsetChange = 0):
        panned = True
        panSize = self.getHorizontalPanSize()
        offset, text = self.getActiveOffsetAndText()
        currline = text.split('\n')[offset['y']]
        newOffsetStart = (int(offset['x']  / panSize) + offsetChange) * panSize
        if newOffsetStart < 0:
            newOffsetStart = 0
            panned = False
        if newOffsetStart >= len(text):
            newOffsetStart = int((len(text) - panSize - 1) / panSize)
            panned = False
        return newOffsetStart, panned    
    def setPanLeft(self):
        newPan, panned = self.getHorizontalPanLevel(-1)
        if self.env['output']['messageOffset']:
            self.env['output']['messageOffset'] = newPan.copy()
        else:
            self.env['output']['cursorOffset'] = newPan.copy()       
        return panned
    def setPanRight(self):
        newPan, panned = self.getHorizontalPanLevel(1)  
        if self.env['output']['messageOffset']:
            self.env['output']['messageOffset'] = newPan.copy()
        else:
            self.env['output']['cursorOffset'] = newPan.copy()            
        return panned
    def removePanning(self):
        if self.env['output']['messageOffset']:
            self.env['output']['messageOffset'] = None
        else:
            self.env['output']['cursorOffset'] = None
    def getBrailleTextWithOffset(self, text, offset = None, cursor = None):
        if text == '':
            return ''
        size = self.env['runtime']['brailleDriver'].getDeviceSize()
        offsetText = text

        if cursor and not offset:
            if self.env['runtime']['settingsManager'].getSetting('braille', 'cursorFollowMode').upper() == 'FIXCELL':
                #fix cell
                cursorCell = self.getFixCursorCell()                                
                offsetStart = cursor['x']      
                if offsetStart < size[0]:        
                    if offsetStart <= cursorCell:
                        return offsetText[0: size[0]]

                offsetStart -= cursorCell
                if offsetStart >= len(offsetText):
                    offsetStart = len(offsetText) - 1
            else: 
                # page and fallback
                offsetStart = int(cursor['x'] / size[0]) * size[0]
        else:
            if not offset:
                offset = {'x':0,'y':0}
            offsetStart = offset['x']         
            if offsetStart >= len(offsetText):
                offsetStart = len(offsetText) - size[0]
        
        if offsetStart < 0:
            offsetStart = 0           
        offsetEnd = offsetStart + size[0]            
        offsetText = offsetText[offsetStart: offsetEnd]        
        return offsetText
    def interruptOutput(self):
        try:
            self.env['runtime']['speechDriver'].cancel()
            self.env['runtime']['debug'].writeDebugOut("Interrupt speech",debug.debugLevel.INFO)       
        except:
            pass            

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
            

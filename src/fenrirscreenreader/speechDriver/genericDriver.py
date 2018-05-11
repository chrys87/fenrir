#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# generic driver

from fenrirscreenreader.core import debug
from threading import Thread, Lock
from queue import Queue, Empty
import shlex
from subprocess import Popen
from fenrirscreenreader.core.speechDriver import speechDriver

class speakQueue(Queue):
    def clear(self):
        try:
            while True:
                self.get_nowait()
        except Empty:
            pass

class driver(speechDriver):
    def __init__(self):
        speechDriver.__init__(self)
        self.proc = None
        self.speechThread = Thread(target=self.worker)
        self.lock = Lock()
        self.textQueue = speakQueue()
    def initialize(self, environment):   
        self.env = environment  
        self.minVolume = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMinVolume')
        self.maxVolume = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMaxVolume')        
        self.minPitch = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMinPitch')        
        self.maxPitch = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMaxPitch')
        self.minRate = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMinRate')
        self.maxRate = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMaxRate')
        
        self.speechCommand = self.env['runtime']['settingsManager'].getSetting('speech', 'genericSpeechCommand')
        if self.speechCommand == '':
            self.speechCommand = 'espeak -a fenrirVolume -s fenrirRate -p fenrirPitch -v fenrirVoice -- "fenrirText"'
        if False: #for debugging overwrite here
            #self.speechCommand = 'spd-say --wait -r 100 -i 100  "fenrirText"'  
            self.speechCommand = 'flite -t "fenrirText"'           
        
        self._isInitialized = True   
        if self._isInitialized:
            self.speechThread.start()   
    def shutdown(self):
        if not self._isInitialized:
            return
        self.cancel()    
        self.textQueue.put(-1)

    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return
        if not queueable: 
            self.cancel()        
        utterance = {
          'text': text,
          'volume': self.volume,
          'rate': self.rate,
          'pitch': self.pitch,
          'module': self.module,
          'language': self.language,
          'voice': self.voice,
        }        
        self.textQueue.put(utterance.copy())

    def cancel(self):
        if not self._isInitialized:
            return
        self.clear_buffer()
        self.lock.acquire(True)
        if self.proc:
            try:
                self.proc.terminate()
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('speechDriver:Cancel:self.proc.terminate():' + str(e),debug.debugLevel.WARNING)                                
                try:
                    self.proc.kill()
                except Exception as e:
                    self.env['runtime']['debug'].writeDebugOut('speechDriver:Cancel:self.proc.kill():' + str(e),debug.debugLevel.WARNING)                    
            self.proc = None            
        self.lock.release()
    def setCallback(self, callback):
        print('SpeechDummyDriver: setCallback')    

    def clear_buffer(self):
        if not self._isInitialized:
            return
        self.textQueue.clear()     
    
    def setVoice(self, voice):
        if not self._isInitialized:
            return
        self.voice = str(voice)

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        self.pitch = str(self.minPitch + pitch * (self.maxPitch - self.minPitch ))

    def setRate(self, rate):
        if not self._isInitialized:
            return
        self.rate = str(self.minRate + rate * (self.maxRate - self.minRate ))

    def setModule(self, module):
        if not self._isInitialized:
            return 
        self.module = str(module)

    def setLanguage(self, language):
        if not self._isInitialized:
            return
        self.language = str(language)

    def setVolume(self, volume):
        if not self._isInitialized:
            return     
        self.volume = str(self.minVolume + volume * (self.maxVolume - self.minVolume ))
    
    def worker(self):
        while True:
            utterance = self.textQueue.get()

            if isinstance(utterance, int):
                if utterance == -1:
                    return
                else:
                    continue
            elif not isinstance(utterance, dict):
                continue
            # no text means nothing to speak
            if not 'text' in utterance:
                continue
            if not isinstance(utterance['text'],str):
                continue            
            if utterance['text'] == '':
                continue
            # check for valid data fields
            if not 'volume' in utterance:
                utterance['volume'] = ''
            if not isinstance(utterance['volume'],str):
                utterance['volume'] = ''
            if not 'module' in utterance:
                utterance['module'] = ''
            if not isinstance(utterance['module'],str):
                utterance['module'] = ''
            if not 'language' in utterance:
                utterance['language'] = ''
            if not isinstance(utterance['language'],str):
                utterance['language'] = ''
            if not 'voice' in utterance:
                utterance['voice'] = ''
            if not isinstance(utterance['voice'],str):
                utterance['voice'] = ''
            if not 'pitch' in utterance:
                utterance['pitch'] = ''
            if not isinstance(utterance['pitch'],str):
                utterance['pitch'] = ''
            if not 'rate' in utterance:
                utterance['rate'] = ''
            if not isinstance(utterance['rate'],str):
                utterance['rate'] = ''

            popenSpeechCommand = shlex.split(self.speechCommand)
            for idx, word in enumerate(popenSpeechCommand):
                word = word.replace('fenrirVolume', str(utterance['volume'] ))
                word = word.replace('fenrirModule', str(utterance['module']))
                word = word.replace('fenrirLanguage', str(utterance['language']))
                word = word.replace('fenrirVoice', str(utterance['voice']))
                word = word.replace('fenrirPitch', str(utterance['pitch']))
                word = word.replace('fenrirRate', str(utterance['rate']))
                word = word.replace('fenrirText', str(utterance['text']))
                popenSpeechCommand[idx] = word

            try:
                self.env['runtime']['debug'].writeDebugOut('speechDriver:worker:' + ' '.join(popenSpeechCommand),debug.debugLevel.INFO)                                            
                self.lock.acquire(True)
                self.proc = Popen(popenSpeechCommand, stdin=None, stdout=None, stderr=None, shell=False)
                self.lock.release()	
                self.proc.wait()
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('speechDriver:worker:' + str(e),debug.debugLevel.ERROR)    

            self.lock.acquire(True)
            self.proc = None
            self.lock.release()


#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# Espeak driver

import subprocess
from fenrirscreenreader.core import debug
from fenrirscreenreader.core.speechDriver import speechDriver

class driver(speechDriver):
    def __init__(self):
        speechDriver.__init__(self)
        self._es = None

    def initialize(self, environment):
        self.env = environment
        try:
            from espeak import espeak 
            self._es = espeak
            self._isInitialized = True
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)
            self._initialized = False

    def speak(self,text, interrupt=True):
        if not self._isInitialized:
            return
        if not interrupt:
            self.cancel()
        if self.voice != None and self.voice != '':
            self._es.set_voice(self.voice)
        elif self.language != None and self.language != '':
            self._es.set_voice(self.language)
        self._es.synth(text)

    def cancel(self):
        if not self._isInitialized:
            return
        self._es.cancel()
        return

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        return self._es.set_parameter(self._es.Parameter().Pitch, int(pitch * 99)) 
        
    def setRate(self, rate):
        if not self._isInitialized:
            return
        return self._es.set_parameter(self._es.Parameter().Rate, int(rate * 899 + 100))

    def setVolume(self, volume):
        if not self._isInitialized:
            return    
        return self._es.set_parameter(self._es.Parameter().Volume, int(volume * 200))

    def setVoice(self, voice):
        if voice == '':
            return
        self.voice = str(voice)
        if self._isInitialized and self._es:
            try:
                self._es.set_voice(self.voice)
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('espeakDriver setVoice:' + str(e), debug.debugLevel.ERROR)

    def getVoices(self):
        if not self._isInitialized:
            self.initialize(self.env)
        voices = []
        if self._isInitialized and self._es:
            try:
                raw_voices = []
                if hasattr(self._es, 'list_voices') and callable(self._es.list_voices):
                    raw_voices = self._es.list_voices()
                elif hasattr(self._es, 'voices'):
                    raw_voices = self._es.voices
                    if callable(raw_voices):
                        raw_voices = raw_voices()
                for v in raw_voices:
                    if hasattr(v, 'name') and v.name:
                        voices.append(str(v.name))
                    elif hasattr(v, 'identifier') and v.identifier:
                        voices.append(str(v.identifier))
                    elif isinstance(v, (list, tuple)) and len(v) > 0:
                        voices.append(str(v[0]))
                    elif isinstance(v, str):
                        voices.append(v)
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('espeakDriver getVoices:' + str(e), debug.debugLevel.ERROR)

        if not voices:
            voices = self._getVoicesFromCli()
        return voices

    def _getVoicesFromCli(self):
        for cmd in ['espeak-ng', 'espeak']:
            try:
                res = subprocess.run([cmd, '--voices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
                if res.returncode == 0 and res.stdout:
                    voices = []
                    lines = res.stdout.strip().splitlines()
                    for line in lines[1:]:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split()
                        if len(parts) >= 4:
                            v_id = parts[1]
                            if v_id not in voices:
                                voices.append(v_id)
                    if voices:
                        return voices
            except Exception:
                pass
        return []

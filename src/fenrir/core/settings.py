#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

settings = {
'sound': {
    'enabled': True,
    'driver': 'generic', 
    'theme': 'default',
    'volume': 1.0,
    'genericPlayFileCommand': 'play -q -v fenrirVolume fenrirSoundFile',
    'genericFrequencyCommand': 'play -q -v fenrirVolume -n -c1 synth fenrirDuration sine fenrirFrequence'
},
'speech':{
    'enabled': True,
    'driver': 'speechd',
    'rate': 0.75,
    'pitch': 0.5,
    'capitalPitch':0.8,
    'volume': 1.0,    
    'module': 'espeak',
    'voice': 'en',
    'language': 'en',
    'autoReadIncoming': True,
},
'braille':{
    'enabled': False, 
    'driver':'brlapi',
    'layout': 'en',
},
'screen':{
    'driver': 'linux',
    'encoding': 'cp850',
    'screenUpdateDelay': 0.4,
    'suspendingScreen': '',
    'autodetectSuspendingScreen': False,
},
'general':{
  'debugLevel': debug.debugLevel.DEACTIVE,
  'punctuationProfile':'default',
  'punctuationLevel': 'some',
  'respectPunctuationPause':True,
  'newLinePause':True,
  'numberOfClipboards': 10,
  'emoticons': True,
  'fenrirKeys': 'KEY_KP0,KEY_META',
  'scriptKeys': 'KEY_COMPOSE',  
  'timeFormat': '%I:%M%P',
  'dateFormat': '%A, %B %d, %Y',
  'autoSpellCheck': False,
  'spellCheckLanguage': 'en_US',
  'scriptPath':'/etc/fenrir/scripts',
},
'focus':{
  'cursor': True,
  'highlight': False,
},
'promote':{
  'enabled': True,
  'inactiveTimeoutSec': 120,
  'list': '',
},
'keyboard':{
  'driver': 'evdev',
  'device': 'all',
  'grabDevices': True,
  'ignoreShortcuts': False,  
  'keyboardLayout': "desktop",
  'charEcho': False,
  'charDeleteEcho': True,
  'wordEcho': True,
  'interruptOnKeyPress': True,
  'doubleTapTimeout': 0.2,
}
}

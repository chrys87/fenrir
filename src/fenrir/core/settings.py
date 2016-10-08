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
    'module': '',
    'voice': 'de',
    'language': 'de',
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
  'punctuationLevel': 1,
  'numberOfClipboards': 10,
  'fenrirKeys': ['KEY_KP0'],
  'timeFormat': '%I:%M%P',
  'dateFormat': '%A, %B %d, %Y',
  'autoSpellCheck': False,
  'spellCheckLanguage': 'en_US',
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
  'doubleTapDelay': 0.2,
}
}

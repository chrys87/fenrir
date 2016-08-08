#!/bin/python

from utils import debug

settings = {
'sound': {
    'enabled': False,
    'driver': 'sox', 
    'theme': 'default',
    'volume':1.0,
},
'speech':{
    'enabled': True,
    'driver':'speechd',
    'rate': 1,
    'pitch': 1,
    'module': '',
    'voice': 'de',
    'language': 'de',
    'volume': 1.0,
    'autoReadIncomming':True,
},
'braille':{
    'enabled': False, 
    'layout': 'en',
},
'screen':{
    'driver': 'linux',
},
'general':{
  'keyboardLayout': "desktop",
  'debugLevel': debug.debugLevel.DEACTIVE,
  'punctuationLevel': 1 
},
'keyboard':{
  'device':"all",
  'keyboardLayout': "desktop",
  'charEcho':False,
  'charDeleteEcho':True,
  'wordEcho':True,
  'interruptOnKeyPress': True,
}
}

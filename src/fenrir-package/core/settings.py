#!/bin/python

from utils import debug

settings = {
'sound': {
    'enabled': False,
    'driver': 'sox', 
    'theme': 'default',
},
'speech':{
    'enabled': True,
    'driver':'speechd',
    'rate': 1,
    'pitch': 1,
    'module': '',
    'voice': 'de',
    'language': 'de',
    'volume': 100
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
  'keyboardLayout': "desktop",
  'charEcho':False,
  'wordEcho':True,
}
}

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
    'rate': 0.75,
    'pitch': 0.5,
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
    'encoding': 'cp850',
    'screenUpdateDelay':0.4,
    'suspendingScreen':'1,2',
    'autodetectSuspendingScreen':False,
},
'general':{
  'keyboardLayout': "desktop",
  'debugLevel': debug.debugLevel.DEACTIVE,
  'punctuationLevel': 1,
  'numberOfClipboards': 10,
  'fenrirKeys':['82'],
  'timeFormat':'%I:%M%P',
  'dateFormat':'%A, %B %d, %Y',
},
'promote':{
  'enabled': True,
  'inactiveTimeoutSec':120,
  'list':'',
},
'keyboard':{
  'device':"all",
  'grabDevices':True,
  'ignoreShortcuts':False,  
  'keyboardLayout': "desktop",
  'charEcho':False,
  'charDeleteEcho':True,
  'wordEcho':True,
  'interruptOnKeyPress': True,
}
}

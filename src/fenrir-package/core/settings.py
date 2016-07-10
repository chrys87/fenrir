#!/bin/python

from utils import debug

settings = {
'speechEnabled': True,
'speechDriverString':'speechd',
'speechRate': 1,
'speechPitch': 1,
'speechModule': '',
'speechVoice': 'de',
'screenDriverString': 'linux',
'keyboardLayout': "desktop",
'brailleEnabled': False, 
'soundEnabled': False,
'soundDriverString': 'sox', 
'soundTheme': 'default',
'debugLevel': debug.debugLevel.DEACTIVE,
'punctuationLevel': 1 
}

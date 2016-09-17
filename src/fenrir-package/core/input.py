#!/bin/python
import time

input = {
'currInput': [],
'prevInput': [], 
'prevDeepestInput': [], 
'currEvent': None, 
'eventBuffer': None,
'shortcutRepeat': 1,
'fenrirKey': ['KEY_KP0'],
'keyForeward': False,
'lastInputTime':time.time(),
'oldNumLock': True,
'newNumLock':True,
'oldCapsLock':False,
'newCapsLock':False
}

inputEvent = {
'EventName': '',
'EventValue': '',
'EventSec': 0,
'EventUsec': 0,
'EventState': 0,
}

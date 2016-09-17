#!/bin/python
import time

input = {
'currInput': [],
'prevInput': [], 
'prevDeepestInput': [], 
'currEvent': None, 
'eventBuffer': None,
'shortcutRepeat': 0,
'fenrirKey': ['82'],
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

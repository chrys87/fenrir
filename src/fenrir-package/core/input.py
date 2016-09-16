#!/bin/python
import time

input = {
'currInput': [],
'prevInput': [], 
'prevDeepestInput': [], 
'currEvent': None, 
'firstEvent': None,
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
'EventTime': time.time(),
'EventState': 0,
}

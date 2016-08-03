#!/bin/python
from _thread import allocate_lock

runtime = {
'speechDriver': None,
'screenDriver': None,
'soundDriver': None,
'brailleDriver': None,
'inputManager': None,
'commandManager': None,
'debug':None,
'globalLock': allocate_lock(),
}

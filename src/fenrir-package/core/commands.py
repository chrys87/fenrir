#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import time


# used as shared memory between commands
# use this in your own commands
commandBuffer = {
'genericList':[],
'genericListSource':'',
'genericListSelection': 0,
'clipboard':[],
'currClipboard': 0,
'Marks':{'1':None, '2':None}
}

# used by the commandManager
commandInfo = {
'currCommand': '',
'lastCommandExecutionTime': time.time(),
'lastCommandRequestTime': time.time()
}

# used by the commandManager
commands = {
'onInput':{
    },
'onScreenChanged':{
    },
'onScreenUpdate':{
    },
'onApplicationChange':{
    },   
'commands':{
    },
'onSwitchApplicationProfile':{
    },
}

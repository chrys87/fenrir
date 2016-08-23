#!/bin/python
import time


# used as shared memory between commands
# use this in your own commands
commandBuffer = {
'clipboard':[],
'currClipboard': 0,
'Marks':{'1':None, '2':None}
}

# used by the commandManager
commandInfo = {
'currCommand': '',
'lastCommandTime': time.time()
}

# used by the commandManager
commands = {
'onInput':{
    },
'onScreenChanged':{
    },
'commands':{
    }
}

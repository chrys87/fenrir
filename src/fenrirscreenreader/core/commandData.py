#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import time

# used as shared memory between commands
# use this in your own commands
commandBuffer = {
'enableSpeechOnKeypress': False,
'Marks':{'1':None, '2':None},
'bookMarks':{},
'windowArea':{},
}

# used by the commandManager
commandInfo = {
#'currCommand': '',
'lastCommandExecutionTime': time.time(),
'lastCommandRequestTime': time.time(),
}

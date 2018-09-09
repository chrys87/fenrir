#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from enum import Enum

class fenrirEventType(Enum):
    Ignore = 0
    StopMainLoop = 1
    ScreenUpdate = 2
    KeyboardInput = 3
    BrailleInput = 4
    PlugInputDevice = 5
    BrailleFlush = 6
    ScreenChanged = 7
    HeartBeat = 8 # for time based scheduling
    ExecuteCommand = 9
    ByteInput = 10
    RemoteIncomming = 11
    def __int__(self):
        return self.value
    def __str__(self):
        return self.name

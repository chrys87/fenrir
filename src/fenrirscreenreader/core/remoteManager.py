#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType

class remoteManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass
    def unixSocketWatchDog():
        pass
    def handleRemoteIncomming(self, eventData):
        if not eventData:
            return

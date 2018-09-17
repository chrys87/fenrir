#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class sayAllManager():
    def __init__(self):
        self.isActive = False
        self.isActiveLock = None
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass
    def setIsActive(self, isActive):
        pass
    def start(self):
        pass
    def isSayAllActive(self):
        pass
    def sayAllWorker(self):
        pass
    def stop(self):
        pass
    def finish(self):
        pass
    def gotoNextPage(self):
        pass

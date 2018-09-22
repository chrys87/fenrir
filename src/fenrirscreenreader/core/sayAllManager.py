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
        if self.isActive:
            self.stop()
    def setIsActive(self, isActive):
        self.isActive = isActive
    def start(self):
        self.setIsActive(True)
    def isSayAllActive(self):
        return self.isActive
    def sayAllWorker(self):
        pass
    def stop(self):
        pass
    def finish(self):
        pass
    def gotoNextPage(self):
        pass

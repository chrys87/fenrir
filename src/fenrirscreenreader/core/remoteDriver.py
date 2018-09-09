#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class remoteDriver():
    def __init__(self):
        self._isInitialized = False
    def initialize(self, environment):
        self.env = environment
        self._isInitialized = True
    def shutdown(self):
        self._isInitialized = False

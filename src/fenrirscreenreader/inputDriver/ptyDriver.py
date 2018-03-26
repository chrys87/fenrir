#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from fenrirscreenreader.core import debug
from fenrirscreenreader.core.inputDriver import inputDriver

class driver(inputDriver):
    def __init__(self):
        inputDriver.__init__(self)
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['inputManager'].setShortcutType('BYTE')
        self._isInitialized = True    

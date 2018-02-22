#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
<<<<<<< HEAD
from core import debug
from core.inputDriver import inputDriver
=======
from fenrir.core import debug
>>>>>>> 1.5

class driver(inputDriver):
    def __init__(self):
        inputDriver.__init__(self)
                
    def getInputEvent(self):
        time.sleep(0.1)
        if not self._initialized:
            return None

#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from core import debug
from core.inputDriver import inputDriver

class driver(inputDriver):
    def __init__(self):
        inputDriver.__init__(self)

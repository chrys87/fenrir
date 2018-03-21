#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.screenDriver import screenDriver

class driver(screenDriver):
    def __init__(self):
        screenDriver.__init__(self)

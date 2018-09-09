#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.remoteDriver import remoteDriver

class driver(remoteDriver):
    def __init__(self):
        remoteDriver.__init__(self)

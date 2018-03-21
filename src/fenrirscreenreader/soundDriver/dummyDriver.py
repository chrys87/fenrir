#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.soundDriver import soundDriver

class driver(soundDriver):
    def __init__(self):
        soundDriver.__init__(self)

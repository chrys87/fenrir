#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from core.soundDriver import soundDriver

class driver(soundDriver):
    def __init__(self):
        soundDriver.__init__(self)

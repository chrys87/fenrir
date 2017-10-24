#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# generic driver

from core import debug
from core.speechDriver import speechDriver
class driver(speechDriver):
    def __init__(self):
        speechDriver.__init__(self)

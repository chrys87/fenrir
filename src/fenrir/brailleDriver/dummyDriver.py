#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from core.brailleDriver import brailleDriver

class driver(brailleDriver):
    def __init__(self):
        brailleDriver.__init__(self)

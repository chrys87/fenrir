#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrir.core import debug
from fenrir.core.brailleDriver import brailleDriver

class driver(brailleDriver):
    def __init__(self):
        brailleDriver.__init__(self)

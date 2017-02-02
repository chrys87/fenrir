#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from core import debug

output = {
'nextFlush': time.time(),
'messageText': '',
'messageOffset': None,
'cursorOffset': None,
}

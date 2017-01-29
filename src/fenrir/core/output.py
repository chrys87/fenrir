#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from core import debug

output = {
'nextFlush': time.time(),
'messageText': '',
'messageOffset': {'x':0,'y':0},
'textOffset': {'x':0,'y':0},
}

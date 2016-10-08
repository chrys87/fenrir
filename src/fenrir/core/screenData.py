#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import time

screenData = {
'columns': 0,
'lines': 0,
'oldDelta': '',
'oldNegativeDelta': '',
'oldCursorReview':None,
'oldCursor':{'x':0,'y':0},
'oldContentBytes': b'',
'oldContentText': '',
'oldContentAttrib': b'',
'oldApplication': '',
'oldTTY':None,
'newDelta': '',
'newNegativeDelta': '',
'newCursorReview':None,
'newCursor':{'x':0,'y':0},
'newContentBytes': b'',
'newContentText': '',
'newContentAttrib': b'',
'newTTY':'0',
'newApplication': '',
'lastScreenUpdate': time.time()
}

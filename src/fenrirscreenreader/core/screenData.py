#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import time

screenData = {
'columns': 0,
'lines': 0,
'oldDelta': '',
'oldAttribDelta': '',
'oldNegativeDelta': '',
'oldCursorReview':None,
'oldCursorAttrib':None,
'oldCursor':{'x':0,'y':0},
'oldContentBytes': b'',
'oldContentText': '',
'oldContentAttrib': None,
'oldApplication': '',
'oldTTY':None,
'newDelta': '',
'newNegativeDelta': '',
'newAttribDelta': '',
'newCursorReview':None,
'newCursorAttrib':None,
'newCursor':{'x':0,'y':0},
'newContentBytes': b'',
'newContentText': '',
'newContentAttrib': None,
'newTTY':'0',
'newApplication': '',
'lastScreenUpdate': time.time(),
'autoIgnoreScreens':[],
}
'''
screenData = {
'columns': 0,
'lines': 0,
'textDelta': '',
'negativeDelta': '',
'attribDelta': '',
'reviewCursor':None, #{'x':0,'y':0}
'attribCursor':None, #{'x':0,'y':0}
'textCursor':None, #{'x':0,'y':0}
'content': None, #{'x':0,'y':0}
'Text': '',
'Attrib': None,
'screen': None,
'application': '',
'timestamp': time.time(),
}
'''

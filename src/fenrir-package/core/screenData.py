#!/bin/python

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
'newDelta': '',
'newNegativeDelta': '',
'newCursorReview':None,
'newCursor':{'x':0,'y':0},
'newContentBytes': b'',
'newContentText': '',
'newContentAttrib': b'',
'oldTTY':'-1',
'newTTY':'0',
'lastScreenUpdate': time.time()
}

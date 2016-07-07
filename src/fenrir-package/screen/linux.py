#!/bin/python

import difflib
import textwrap
import time

#import fenrir.utils.debug
class screenManager():
    def __init__(self, device='/dev/vcsa'):
        self.vcsaDevice = device

    def analyzeScreen(self, runtime):
        # read screen
        currTTY = open('/sys/devices/virtual/tty/tty0/active','r')
        runtime['newTTY'] = currTTY.read()[3:-1]
        currTTY.close() 
        
        try:
            vcsa = open(self.vcsaDevice + runtime['newTTY'] ,'rb',0)
            runtime['newContentBytes'] = vcsa.read()
            vcsa.close()
        except:
            return runtime

        # get metadata like cursor or screensize
        runtime['lines'] = int( runtime['newContentBytes'][0])
        runtime['columns'] = int( runtime['newContentBytes'][1])
        runtime['newCursor']['x'] = int( runtime['newContentBytes'][2])
        runtime['newCursor']['y'] = int( runtime['newContentBytes'][3])

        # analyze content
        runtime['newContentText'] = str(runtime['newContentBytes'][4:][::2].decode('cp1252').encode('utf-8'))[2:]
        runtime['newContentAttrib'] = runtime['newContentBytes'][5:][::2]
        runtime['newContentText'] = '\n'.join(textwrap.wrap(runtime['newContentText'], runtime['columns']))[:-2]
        
        if runtime['newTTY'] != runtime['oldTTY']:
            runtime['oldContentBytes'] = b''
            runtime['oldContentAttrib'] = b''
            runtime['oldContentText'] = ''
            runtime['oldCursor']['x'] = 0
            runtime['oldCursor']['y'] = 0

        # changes on the screen
        if runtime['oldContentBytes'] != runtime['newContentBytes']:
            if ((len(runtime['delta']) < 4) or runtime['oldTTY'] != runtime['newTTY']):
                runtime['speechDriver'].cancel()
            diff = difflib.ndiff(runtime['oldContentText'], runtime['newContentText'])
            runtime['delta'] = ''.join(x[2:] for x in diff if x.startswith('+ '))
            runtime['speechDriver'].speak(runtime['delta'])

            # set new "old" values
            runtime['oldContentBytes'] = runtime['newContentBytes']
            runtime['oldContentText'] = runtime['newContentText']
            runtime['oldContentTextAttrib'] = runtime['newContentAttrib']
            runtime['oldCursor']['x'] = runtime['newCursor']['x']
            runtime['oldCursor']['y'] = runtime['newCursor']['y']
            runtime['oldTTY'] = runtime['newTTY']
        return runtime

#!/bin/python
# -*- coding: utf-8 -*-

import difflib
import textwrap
import time
import re

#import fenrir.utils.debug
class screenManager():
    def __init__(self, device='/dev/vcsa'):
        self.vcsaDevicePath = device

    def analyzeScreen(self, environment):
        # read screen
        currTTY = open('/sys/devices/virtual/tty/tty0/active','r')
        environment['screenData']['newTTY'] = currTTY.read()[3:-1]
        currTTY.close() 
        
        try:
            vcsa = open(self.vcsaDevicePath + environment['screenData']['newTTY'] ,'rb',0)
            environment['screenData']['newContentBytes'] = vcsa.read()
            vcsa.close()
        except:
            return environment

        # get metadata like cursor or screensize
        environment['screenData']['lines'] = int( environment['screenData']['newContentBytes'][0])
        environment['screenData']['columns'] = int( environment['screenData']['newContentBytes'][1])
        environment['screenData']['newCursor']['x'] = int( environment['screenData']['newContentBytes'][2])
        environment['screenData']['newCursor']['y'] = int( environment['screenData']['newContentBytes'][3])

        # analyze content
        environment['screenData']['newContentText'] = str(environment['screenData']['newContentBytes'][4:][::2].decode('WINDOWS-1250'))
        #environment['screenData']['newContentText'] = str(environment['screenData']['newContentBytes'][4:][::2].decode('cp1252')).encode('utf-8')[2:]
        environment['screenData']['newContentAttrib'] = environment['screenData']['newContentBytes'][5:][::2]
        #environment['screenData']['newContentText'] = '\n'.join(textwrap.wrap(environment['screenData']['newContentText'], environment['screenData']['columns']))[:-2]
        environment['screenData']['newContentText'] =  re.sub("(.{"+ str(environment['screenData']['columns'])+"})", "\\1\n", str(environment['screenData']['newContentText']), 0, re.DOTALL)

        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            environment['screenData']['oldContentBytes'] = b''
            environment['screenData']['oldContentAttrib'] = b''
            environment['screenData']['oldContentText'] = ''
            environment['screenData']['oldCursor']['x'] = 0
            environment['screenData']['oldCursor']['y'] = 0

        # changes on the screen
        if environment['screenData']['oldContentBytes'] != environment['screenData']['newContentBytes']:
            if ((len(environment['screenData']['delta']) < 4) or environment['screenData']['oldTTY'] != environment['screenData']['newTTY']):
                environment['runtime']['speechDriver'].cancel()
            diff = difflib.ndiff(environment['screenData']['oldContentText'], environment['screenData']['newContentText'])
            environment['screenData']['delta'] = ''.join(x[2:] for x in diff if x.startswith('+ '))
            environment['runtime']['speechDriver'].speak(environment['screenData']['delta'])
            # set new "old" values
            environment['screenData']['oldContentBytes'] = environment['screenData']['newContentBytes']
            environment['screenData']['oldContentText'] = environment['screenData']['newContentText']
            environment['screenData']['oldContentTextAttrib'] = environment['screenData']['newContentAttrib']
            environment['screenData']['oldCursor']['x'] = environment['screenData']['newCursor']['x']
            environment['screenData']['oldCursor']['y'] = environment['screenData']['newCursor']['y']
            environment['screenData']['oldTTY'] = environment['screenData']['newTTY']
        return environment

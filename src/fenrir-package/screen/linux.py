#!/bin/python
# -*- coding: utf-8 -*-

import difflib
import time
import re

#import fenrir.utils.debug
class screen():
    def __init__(self, device='/dev/vcsa'):
        self.vcsaDevicePath = device

    def insert_newlines(self, string, every=64):
        return '\n'.join(string[i:i+every] for i in range(0, len(string), every))
            
    def analyzeScreen(self, environment, trigger='updateScreen'):
        newTTY = ''
        newContentBytes = b''       
        try:
            # read screen
            currTTY = open('/sys/devices/virtual/tty/tty0/active','r')
            newTTY = currTTY.read()[3:-1]
            currTTY.close() 
            vcsa = open(self.vcsaDevicePath + newTTY,'rb',0)
            newContentBytes = vcsa.read()
            vcsa.close()
            if len(newContentBytes) < 5:
                return environment
        except:
            return environment
        screenEncoding = environment['runtime']['settingsManager'].getSetting(environment,'screen', 'encoding')
        # set new "old" values
        environment['screenData']['oldContentBytes'] = environment['screenData']['newContentBytes']
        environment['screenData']['oldContentText'] = environment['screenData']['newContentText']
        environment['screenData']['oldContentTextAttrib'] = environment['screenData']['newContentAttrib']
        environment['screenData']['oldCursor']['x'] = environment['screenData']['newCursor']['x']
        environment['screenData']['oldCursor']['y'] = environment['screenData']['newCursor']['y']
        if environment['screenData']['oldTTY'] == '-1':
            environment['screenData']['oldTTY'] = newTTY # dont recognice starting fenrir as change
        else:    
            environment['screenData']['oldTTY'] = environment['screenData']['newTTY']
        environment['screenData']['oldDelta'] = environment['screenData']['newDelta']
        environment['screenData']['oldNegativeDelta'] = environment['screenData']['newNegativeDelta']
        environment['screenData']['newTTY'] = newTTY
        environment['screenData']['newContentBytes'] = newContentBytes
        # get metadata like cursor or screensize
        environment['screenData']['lines'] = int( environment['screenData']['newContentBytes'][0])
        environment['screenData']['columns'] = int( environment['screenData']['newContentBytes'][1])
        environment['screenData']['newCursor']['x'] = int( environment['screenData']['newContentBytes'][2])
        environment['screenData']['newCursor']['y'] = int( environment['screenData']['newContentBytes'][3])
        # analyze content
        environment['screenData']['newContentText'] = environment['screenData']['newContentBytes'][4:][::2].decode(screenEncoding, "replace").encode('utf-8').decode('utf-8')
        environment['screenData']['newContentAttrib'] = environment['screenData']['newContentBytes'][5:][::2]
        #environment['screenData']['newContentText'] = '\n'.join(self.textWrapper.wrap(environment['screenData']['newContentText'], ))[:-2]
        environment['screenData']['newContentText'] = self.insert_newlines(environment['screenData']['newContentText'], environment['screenData']['columns'])

        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            environment['screenData']['oldContentBytes'] = b''
            environment['screenData']['oldContentAttrib'] = b''
            environment['screenData']['oldContentText'] = ''
            environment['screenData']['oldCursor']['x'] = 0
            environment['screenData']['oldCursor']['y'] = 0
            environment['screenData']['oldDelta'] = ''
            environment['screenData']['newDelta'] = ''
            environment['screenData']['oldNegativeDelta'] = ''
            environment['screenData']['newNegativeDelta'] = ''
        
        # changes on the screen
        if (environment['screenData']['oldContentText'] != environment['screenData']['newContentText']) and \
          (environment['screenData']['newContentText'] != '' ):
            if environment['screenData']['oldContentText'] == '' and\
              environment['screenData']['newContentText'] != '':
                environment['screenData']['newDelta'] = environment['screenData']['newContentText']  
            else:
                diffStart = 0
                if environment['screenData']['oldCursor']['x'] != environment['screenData']['newCursor']['x'] and \
                  environment['screenData']['oldCursor']['y'] == environment['screenData']['newCursor']['y'] and \
                  environment['screenData']['newContentText'][:environment['screenData']['newCursor']['y']] == environment['screenData']['oldContentText'][:environment['screenData']['newCursor']['y']]:
                    diffStart = environment['screenData']['newCursor']['y'] * environment['screenData']['newCursor']['x'] + environment['screenData']['newCursor']['y']
                    diff = difflib.ndiff(environment['screenData']['oldContentText'][diffStart:],\
                      environment['screenData']['newContentText'][diffStart:])      
                else:
                   diff = difflib.ndiff( environment['screenData']['oldContentText'][diffStart:].split('\n'),\
                     environment['screenData']['newContentText'][diffStart:].split('\n'))
                
                diffList = list(diff)

                environment['screenData']['newDelta'] = ''.join(x[2:] for x in diffList if x.startswith('+ '))             
                environment['screenData']['newNegativeDelta'] = ''.join(x[2:] for x in diffList if x.startswith('- '))
        else:
            environment['screenData']['newNegativeDelta'] = ''
            environment['screenData']['newDelta'] = ''           
        return environment

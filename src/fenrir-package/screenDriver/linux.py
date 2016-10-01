#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import difflib
import re
import subprocess
from core import debug

class driver():
    def __init__(self):
        self.vcsaDevicePath = '/dev/vcsa'
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def insert_newlines(self, string, every=64):
        return '\n'.join(string[i:i+every] for i in range(0, len(string), every))
    
    def getCurrScreen(self):
        self.env['screenData']['oldTTY'] = self.env['screenData']['newTTY']
        try:    
            currScreenFile = open('/sys/devices/virtual/tty/tty0/active','r')
            self.env['screenData']['newTTY'] = str(currScreenFile.read()[3:-1])
            currScreenFile.close()
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)   

    def getCurrApplication(self):
        apps = []
        try:
            currScreen = self.env['screenData']['newTTY']
            apps = subprocess.Popen('ps -t tty' + currScreen + ' -o comm,tty,stat', shell=True, stdout=subprocess.PIPE).stdout.read().decode()[:-1].split('\n')
        except Exception as e:
            print(e)
            return ''

        try:
            for i in apps:
                i = i.upper()
                i = i.split()
                i[0] = i[0]
                i[1] = i[1]
                if '+' in i[2]:
                    if i[0] != '':
                        if not "GREP" == i[0] and \
                          not "SH" == i[0] and \
                          not "PS" == i[0]:
                            if "TTY"+currScreen in i[1]:
                                if self.env['runtime']['applicationManager'].isApplicationChange():
                                    self.env['screenData']['oldApplication'] = self.env['screenData']['newApplication']
                                    self.env['screenData']['newApplication'] = i[0]                                 
                                return
        except:
            return ''
        return ''

    def getIgnoreScreens(self):
        xlist = []
        try:
            x = subprocess.Popen('ps a -o tty,comm | grep Xorg', shell=True, stdout=subprocess.PIPE).stdout.read().decode()[:-1].split('\n')
        except Exception as e:
            print(e)
            return xlist
        for i in x:
            if not "grep" in i and \
              not "ps" in i:                
                if (i[:3].lower() == 'tty'):
                    xlist.append(i[3])
        return xlist


    def update(self, trigger='updateScreen'):
        newContentBytes = b''       
        try:
            # read screen
            vcsa = open(self.vcsaDevicePath + self.env['screenData']['newTTY'],'rb',0)
            newContentBytes = vcsa.read()
            vcsa.close()
            if len(newContentBytes) < 5:
                return
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)   
            return
        screenEncoding = self.env['runtime']['settingsManager'].getSetting('screen', 'encoding')
        # set new "old" values
        self.env['screenData']['oldContentBytes'] = self.env['screenData']['newContentBytes']
        self.env['screenData']['oldContentText'] = self.env['screenData']['newContentText']
        self.env['screenData']['oldContentTextAttrib'] = self.env['screenData']['newContentAttrib']
        self.env['screenData']['oldCursor']['x'] = self.env['screenData']['newCursor']['x']
        self.env['screenData']['oldCursor']['y'] = self.env['screenData']['newCursor']['y']
        self.env['screenData']['oldDelta'] = self.env['screenData']['newDelta']
        self.env['screenData']['oldNegativeDelta'] = self.env['screenData']['newNegativeDelta']
        self.env['screenData']['newContentBytes'] = newContentBytes
        # get metadata like cursor or screensize
        self.env['screenData']['lines'] = int( self.env['screenData']['newContentBytes'][0])
        self.env['screenData']['columns'] = int( self.env['screenData']['newContentBytes'][1])
        self.env['screenData']['newCursor']['x'] = int( self.env['screenData']['newContentBytes'][2])
        self.env['screenData']['newCursor']['y'] = int( self.env['screenData']['newContentBytes'][3])
        # analyze content
        self.env['screenData']['newContentText'] = self.env['screenData']['newContentBytes'][4:][::2].decode(screenEncoding, "replace").encode('utf-8').decode('utf-8')
        self.env['screenData']['newContentAttrib'] = self.env['screenData']['newContentBytes'][5:][::2]
        self.env['screenData']['newContentText'] = self.insert_newlines(self.env['screenData']['newContentText'], self.env['screenData']['columns'])

        if self.env['screenData']['newTTY'] != self.env['screenData']['oldTTY']:
            self.env['screenData']['oldContentBytes'] = b''
            self.env['screenData']['oldContentAttrib'] = b''
            self.env['screenData']['oldContentText'] = ''
            self.env['screenData']['oldCursor']['x'] = 0
            self.env['screenData']['oldCursor']['y'] = 0
            self.env['screenData']['oldDelta'] = ''
            self.env['screenData']['oldNegativeDelta'] = ''
        # always clear current deltas
        self.env['screenData']['newNegativeDelta'] = ''
        self.env['screenData']['newDelta'] = ''                   
        # changes on the screen
        oldScreenText = re.sub(' +',' ',self.env['runtime']['screenManager'].getWindowAreaInText(self.env['screenData']['oldContentText']))
        newScreenText = re.sub(' +',' ',self.env['runtime']['screenManager'].getWindowAreaInText(self.env['screenData']['newContentText']))        
        if (self.env['screenData']['oldContentText'] != self.env['screenData']['newContentText']) and \
          (self.env['screenData']['newContentText'] != '' ):
            if oldScreenText == '' and\
              newScreenText != '':
                self.env['screenData']['newDelta'] = newScreenText
            else:
                diffStart = 0
                if self.env['screenData']['oldCursor']['x'] != self.env['screenData']['newCursor']['x'] and \
                  self.env['screenData']['oldCursor']['y'] == self.env['screenData']['newCursor']['y'] and \
                  self.env['screenData']['newContentText'][:self.env['screenData']['newCursor']['y']] == self.env['screenData']['oldContentText'][:self.env['screenData']['newCursor']['y']]:
                    diffStart = self.env['screenData']['newCursor']['y'] * self.env['screenData']['columns'] + self.env['screenData']['newCursor']['y']
                    oldScreenText = self.env['screenData']['oldContentText'][diffStart:diffStart  + self.env['screenData']['columns']] 
                    oldScreenText = re.sub(' +',' ',oldScreenText)
                    newScreenText = self.env['screenData']['newContentText'][diffStart:diffStart  + self.env['screenData']['columns']]
                    newScreenText = re.sub(' +',' ',newScreenText)
                    diff = difflib.ndiff(oldScreenText, newScreenText)      
                else:
                    diff = difflib.ndiff( oldScreenText.split('\n'),\
                      newScreenText.split('\n'))

                diffList = list(diff)
                
                self.env['screenData']['newDelta'] = ''.join(x[2:] for x in diffList if x.startswith('+ '))             
                self.env['screenData']['newNegativeDelta'] = ''.join(x[2:] for x in diffList if x.startswith('- '))

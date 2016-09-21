#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import difflib
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
        currScreen = -1
        try:    
            currScreenFile = open('/sys/devices/virtual/tty/tty0/active','r')
            currScreen = currScreenFile.read()[3:-1]
            currScreenFile.close()
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)   
        return currScreen

    def getCurrApplication(self, screen):
        apps = []
        appList = []
        try:
            apps = subprocess.Popen('ps a -o comm,tty,stat', shell=True, stdout=subprocess.PIPE).stdout.read().decode()[:-1].split('\n')
        except Exception as e:
            print(e)
            return appList
        currScreen = str(screen)
        for i in apps:
            i = i.split()
            i[0] = i[0].lower()
            i[1] = i[1].lower()
            if '+' in i[2]:
                if not "grep" == i[0] and \
                  not "sh" == i[0] and \
                  not "ps" == i[0]:
                    if "tty"+currScreen in i[1]:
                        appList.append(i[0])
        return appList

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
        newTTY = ''
        newContentBytes = b''       
        try:
            # read screen
            newTTY = self.getCurrScreen()
            vcsa = open(self.vcsaDevicePath + newTTY,'rb',0)
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
        if self.env['screenData']['oldTTY'] == '-1':
            self.env['screenData']['oldTTY'] = newTTY # dont recognice starting fenrir as change
        else:    
            self.env['screenData']['oldTTY'] = self.env['screenData']['newTTY']
        self.env['screenData']['oldDelta'] = self.env['screenData']['newDelta']
        self.env['screenData']['oldNegativeDelta'] = self.env['screenData']['newNegativeDelta']
        self.env['screenData']['oldApplication'] = self.env['screenData']['newApplication'] 
        self.env['screenData']['newTTY'] = newTTY
        self.env['screenData']['newContentBytes'] = newContentBytes
        # get metadata like cursor or screensize
        self.env['screenData']['lines'] = int( self.env['screenData']['newContentBytes'][0])
        self.env['screenData']['columns'] = int( self.env['screenData']['newContentBytes'][1])
        self.env['screenData']['newCursor']['x'] = int( self.env['screenData']['newContentBytes'][2])
        self.env['screenData']['newCursor']['y'] = int( self.env['screenData']['newContentBytes'][3])
        self.env['screenData']['newApplication'] = self.getCurrApplication(newTTY)
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
            self.env['screenData']['oldApplication'] = ''
        # always clear current deltas
        self.env['screenData']['newNegativeDelta'] = ''
        self.env['screenData']['newDelta'] = ''                   
        # changes on the screen
        if (self.env['screenData']['oldContentText'] != self.env['screenData']['newContentText']) and \
          (self.env['screenData']['newContentText'] != '' ):
            if self.env['screenData']['oldContentText'] == '' and\
              self.env['screenData']['newContentText'] != '':
                self.env['screenData']['newDelta'] = self.env['screenData']['newContentText']  
            else:
                diffStart = 0
                if self.env['screenData']['oldCursor']['x'] != self.env['screenData']['newCursor']['x'] and \
                  self.env['screenData']['oldCursor']['y'] == self.env['screenData']['newCursor']['y'] and \
                  self.env['screenData']['newContentText'][:self.env['screenData']['newCursor']['y']] == self.env['screenData']['oldContentText'][:self.env['screenData']['newCursor']['y']]:
                    diffStart = self.env['screenData']['newCursor']['y'] * self.env['screenData']['columns'] + self.env['screenData']['newCursor']['y']
                    diff = difflib.ndiff(self.env['screenData']['oldContentText'][diffStart:diffStart  + self.env['screenData']['columns']],\
                      self.env['screenData']['newContentText'][diffStart:diffStart  + self.env['screenData']['columns']])      
                else:
                   diff = difflib.ndiff( self.env['screenData']['oldContentText'][diffStart:].split('\n'),\
                     self.env['screenData']['newContentText'][diffStart:].split('\n'))
                
                diffList = list(diff)

                self.env['screenData']['newDelta'] = ''.join(x[2:] for x in diffList if x.startswith('+ '))             
                self.env['screenData']['newNegativeDelta'] = ''.join(x[2:] for x in diffList if x.startswith('- '))

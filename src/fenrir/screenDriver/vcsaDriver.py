#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import difflib
import re
import subprocess
import fcntl
import termios
import time
import dbus
from core import debug
from utils import screen_utils

class driver():
    def __init__(self):
        self.vcsaDevicePath = '/dev/vcsa'
        self.ListSessions = None
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getCurrScreen(self):
        self.env['screenData']['oldTTY'] = self.env['screenData']['newTTY']
        try:    
            currScreenFile = open('/sys/devices/virtual/tty/tty0/active','r')
            self.env['screenData']['newTTY'] = str(currScreenFile.read()[3:-1])
            currScreenFile.close()
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)   
    def injectTextToScreen(self, text, screen = None):
        useScreen = "/dev/tty" + self.env['screenData']['newTTY']
        if screen != None:
            useScreen = screen
        with open(useScreen, 'w') as fd:
            for c in text:
                fcntl.ioctl(fd, termios.TIOCSTI, c)
                
    def getCurrApplication(self):
        apps = []
        try:
            currScreen = self.env['screenData']['newTTY']
            apps = subprocess.Popen('ps -t tty' + currScreen + ' -o comm,tty,stat', shell=True, stdout=subprocess.PIPE).stdout.read().decode()[:-1].split('\n')
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)         
            return
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
                                if self.env['screenData']['newApplication'] != i[0]:
                                    self.env['screenData']['newApplication'] = i[0]                        
                                return
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)    

    def getSessionInformation(self):
        bus = dbus.SystemBus()
        if not self.ListSessions:
            obj  = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
            inf = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
            self.ListSessions = inf.get_dbus_method('ListSessions')
    
        sessions = self.ListSessions()
        self.env['screenData']['autoIgnoreScreens'] = []
        for session in sessions:
            obj = bus.get_object('org.freedesktop.login1', session[4])
            inf = dbus.Interface(obj, 'org.freedesktop.DBus.Properties')
            sessionType = inf.Get('org.freedesktop.login1.Session', 'Type')
            screen = str(inf.Get('org.freedesktop.login1.Session', 'VTNr'))  
            if screen == '':                      
                screen = str(inf.Get('org.freedesktop.login1.Session', 'TTY'))
                screen = screen[screen.upper().find('TTY') + 3:]
            if screen == '':
                self.env['runtime']['debug'].writeDebugOut('No TTY found for session:' + session[4],debug.debugLevel.ERROR)               
                return
            if sessionType.upper() == 'X11':
                self.env['screenData']['autoIgnoreScreens'].append(screen)
            if screen == self.env['screenData']['newTTY'] :
                if self.env['generalInformation']['currUser'] != session[2]:
                    self.env['generalInformation']['prevUser'] = self.env['generalInformation']['currUser']
                    self.env['generalInformation']['currUser'] = session[2]

    def update(self, trigger='onUpdate'):
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
        self.env['screenData']['oldContentAttrib'] = self.env['screenData']['newContentAttrib']
        self.env['screenData']['oldCursor'] = self.env['screenData']['newCursor'].copy()
        if self.env['screenData']['newCursorAttrib']:
            self.env['screenData']['oldCursorAttrib'] = self.env['screenData']['newCursorAttrib'].copy()        
        self.env['screenData']['oldDelta'] = self.env['screenData']['newDelta']
        self.env['screenData']['oldAttribDelta'] = self.env['screenData']['newAttribDelta']
        self.env['screenData']['oldNegativeDelta'] = self.env['screenData']['newNegativeDelta']
        self.env['screenData']['newContentBytes'] = newContentBytes
        # get metadata like cursor or screensize
        self.env['screenData']['lines'] = int( self.env['screenData']['newContentBytes'][0])
        self.env['screenData']['columns'] = int( self.env['screenData']['newContentBytes'][1])
        self.env['screenData']['newCursor']['x'] = int( self.env['screenData']['newContentBytes'][2])
        self.env['screenData']['newCursor']['y'] = int( self.env['screenData']['newContentBytes'][3])
        # analyze content
        self.env['screenData']['newContentText'] = self.env['screenData']['newContentBytes'][4:][::2].decode(screenEncoding, "replace").encode('utf-8').decode('utf-8')
        self.env['screenData']['newContentText'] = screen_utils.removeNonprintable(self.env['screenData']['newContentText'])
        self.env['screenData']['newContentAttrib'] = self.env['screenData']['newContentBytes'][5:][::2]
        self.env['screenData']['newContentText'] = screen_utils.insertNewlines(self.env['screenData']['newContentText'], self.env['screenData']['columns'])

        if self.env['screenData']['newTTY'] != self.env['screenData']['oldTTY']:
            self.env['screenData']['oldContentBytes'] = b''
            self.env['screenData']['oldContentAttrib'] = b''
            self.env['screenData']['oldContentText'] = ''
            self.env['screenData']['oldCursor']['x'] = 0
            self.env['screenData']['oldCursor']['y'] = 0
            self.env['screenData']['oldDelta'] = ''
            self.env['screenData']['oldAttribDelta'] = ''            
            self.env['screenData']['oldCursorAttrib'] = None
            self.env['screenData']['newCursorAttrib'] = None            
            self.env['screenData']['oldNegativeDelta'] = ''
        # initialize current deltas
        self.env['screenData']['newNegativeDelta'] = ''
        self.env['screenData']['newDelta'] = ''
        self.env['screenData']['newAttribDelta'] = ''                           

        # changes on the screen
        oldScreenText = re.sub(' +',' ',self.env['runtime']['screenManager'].getWindowAreaInText(self.env['screenData']['oldContentText']))
        newScreenText = re.sub(' +',' ',self.env['runtime']['screenManager'].getWindowAreaInText(self.env['screenData']['newContentText']))        
        typing = False
        if (self.env['screenData']['oldContentText'] != self.env['screenData']['newContentText']) and \
          (self.env['screenData']['newContentText'] != '' ):
            if oldScreenText == '' and\
              newScreenText != '':
                self.env['screenData']['newDelta'] = newScreenText
            else:
                cursorLineStart = self.env['screenData']['newCursor']['y'] * self.env['screenData']['columns'] + self.env['screenData']['newCursor']['y']
                cursorLineEnd = cursorLineStart  + self.env['screenData']['columns']            
                if self.env['screenData']['oldCursor']['x'] != self.env['screenData']['newCursor']['x'] and \
                  self.env['screenData']['oldCursor']['y'] == self.env['screenData']['newCursor']['y'] and \
                  self.env['screenData']['newContentText'][:cursorLineStart] == self.env['screenData']['oldContentText'][:cursorLineStart]:

                    oldScreenText = self.env['screenData']['oldContentText'][cursorLineStart:cursorLineEnd] 
                    oldScreenText = re.sub(' +',' ',oldScreenText)
                    newScreenText = self.env['screenData']['newContentText'][cursorLineStart:cursorLineEnd]
                    newScreenText = re.sub(' +',' ',newScreenText)
                    diff = difflib.ndiff(oldScreenText, newScreenText) 
                    typing = True                      
                else:
                    diff = difflib.ndiff( oldScreenText.split('\n'),\
                      newScreenText.split('\n'))

                diffList = list(diff)
                
                if self.env['runtime']['settingsManager'].getSetting('general', 'newLinePause') and not typing:
                    self.env['screenData']['newDelta'] = '\n'.join(x[2:] for x in diffList if x[0] == '+')
                else:
                    self.env['screenData']['newDelta'] = ''.join(x[2:] for x in diffList if x[0] == '+')             
                self.env['screenData']['newNegativeDelta'] = ''.join(x[2:] for x in diffList if x[0] == '-')
        
        # track highlighted
        if self.env['screenData']['oldContentAttrib'] != self.env['screenData']['newContentAttrib']:
            if self.env['runtime']['settingsManager'].getSettingAsBool('focus', 'highlight'):
                self.env['screenData']['newAttribDelta'], self.env['screenData']['newCursorAttrib'] = screen_utils.trackHighlights(self.env['screenData']['oldContentAttrib'], self.env['screenData']['newContentAttrib'], self.env['screenData']['newContentText'], self.env['screenData']['columns'])
                

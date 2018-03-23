#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
#attrib:
#http://rampex.ihep.su/Linux/linux_howto/html/tutorials/mini/Colour-ls-6.html
#0 = black, 1 = blue, 2 = green, 3 = cyan, 4 = red, 5 = purple, 6 = brown/yellow, 7 = white. 
#https://github.com/jwilk/vcsapeek/blob/master/linuxvt.py
#blink = 5 if attr & 1 else 0
#bold = 1 if attr & 16 else 0

import subprocess
import glob, os
import termios
import time
import select
import dbus
import fcntl
from array import array
from fenrirscreenreader.utils import screen_utils
from fcntl import ioctl
from struct import unpack_from, unpack, pack
from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType
from fenrirscreenreader.core.screenDriver import screenDriver

class driver(screenDriver):
    def __init__(self):
        screenDriver.__init__(self)
        self.ListSessions = None
        self.charmap = {}
        self.bgColorNames = {0: _('black'), 1: _('blue'), 2: _('green'), 3: _('cyan'), 4: _('red'), 5: _('Magenta'), 6: _('brown/yellow'), 7: _('white')}
        self.fgColorNames = {0: _('Black'), 1: _('Blue'), 2: _('Green'), 3: _('Cyan'), 4: _('Red'), 5: _('Magenta'), 6: _('brown/yellow'), 7: _('Light gray'), 8: _('Dark gray'), 9: _('Light blue'), 10: ('Light green'), 11: _('Light cyan'), 12: _('Light red'), 13: _('Light magenta'), 14: _('Light yellow'), 15: _('White')}
        self.hichar = None        
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['processManager'].addCustomEventThread(self.updateWatchdog)        
    def getCurrScreen(self):
        self.env['screen']['oldTTY'] = self.env['screen']['newTTY']
        self.env['screen']['newTTY'] = str(1)
 
    def injectTextToScreen(self, text, screen = None):
        pass
                
    def getSessionInformation(self):
        self.env['screen']['autoIgnoreScreens'] = []
        self.env['general']['prevUser'] = 'chrys'
        self.env['general']['currUser'] = 'chrys'

    def updateWatchdog(self,active , eventQueue):
        pass

    def createScreenEventData(self, screen, content, attribute):
        self.updateCharMap(screen)                                
        eventData = {
            'bytes': content,
            'lines': int( content[0]),
            'columns': int( content[1]),
            'textCursor': 
                {
                    'x': int( content[2]),
                    'y': int( content[3])
                },
            'screen': screen,     
            'screenUpdateTime': time.time(),            
        }
        #encText, encAttr =\
        #  self.autoDecodeVCSA(content[4:], eventData['lines'], eventData['columns'])
        eventData['text'] = content
        eventData['attributes'] = attribute
        return eventData.copy()     

    def getFenrirBGColor(self, attribute):
        try:
            return self.bgColorNames[attribute[2]]
        except Exception as e:
            print(e)
            return ''
    def getFenrirFGColor(self, attribute):
        try:
            return self.fgColorNames[attribute[1]]
        except Exception as e:
            print(e)        
            return ''
    def getFenrirUnderline(self, attribute):
        if attribute[5] == 1:
            return _('underlined')
        return ''    
    def getFenrirBold(self, attribute):
        if attribute[4] == 1:
            return _('bold')    
        return ''    
    def getFenrirBlink(self, attribute):
        if attribute[3] == 1:
            return _('blink')    
        return ''    
    def getFenrirFont(self, attribute):
        return _('Default')
    def getFenrirFontSize(self, attribute):
        return _('Default')              
    def getCurrApplication(self):
        pass

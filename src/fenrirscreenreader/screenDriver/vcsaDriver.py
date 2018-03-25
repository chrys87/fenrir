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
        self.env['runtime']['processManager'].addCustomEventThread(self.updateWatchdog, multiprocess=True)        
    def getCurrScreen(self):
        self.env['screen']['oldTTY'] = self.env['screen']['newTTY']
        try:    
            currScreenFile = open('/sys/devices/virtual/tty/tty0/active','r')
            self.env['screen']['newTTY'] = str(currScreenFile.read()[3:-1])
            currScreenFile.close()
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)   
    def injectTextToScreen(self, text, screen = None):
        useScreen = "/dev/tty" + self.env['screen']['newTTY']
        if screen != None:
            useScreen = screen
        with open(useScreen, 'w') as fd:
            for c in text:
                fcntl.ioctl(fd, termios.TIOCSTI, c)
                
    def getSessionInformation(self):
        try:
            bus = dbus.SystemBus()
            if not self.ListSessions:
                obj  = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
                inf = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
                self.ListSessions = inf.get_dbus_method('ListSessions')
            sessions = self.ListSessions()
            self.env['screen']['autoIgnoreScreens'] = []
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
                if sessionType.upper() != 'TTY':
                    self.env['screen']['autoIgnoreScreens'].append(screen)
                if screen == self.env['screen']['newTTY'] :
                    if self.env['general']['currUser'] != session[2]:
                        self.env['general']['prevUser'] = self.env['general']['currUser']
                        self.env['general']['currUser'] = session[2]                                                                
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('getSessionInformation: Maybe no LoginD:' + str(e),debug.debugLevel.ERROR)               
            self.env['screen']['autoIgnoreScreens'] = []     
        #self.env['runtime']['debug'].writeDebugOut('getSessionInformation:'  + str(self.env['screen']['autoIgnoreScreens']) + ' ' + str(self.env['general'])  ,debug.debugLevel.INFO)                           

    def updateWatchdog(self,active , eventQueue):
        try:
            vcsa = {}
            vcsaDevices = glob.glob('/dev/vcsa*')
            for vcsaDev in vcsaDevices:
                index = vcsaDev[9:]
                vcsa[str(index)] = open(vcsaDev,'rb')

            tty = open('/sys/devices/virtual/tty/tty0/active','r')
            currScreen = str(tty.read()[3:-1])
            oldScreen = currScreen
            watchdog = select.epoll()
            watchdog.register(vcsa[currScreen], select.POLLPRI | select.POLLERR)
            watchdog.register(tty, select.POLLPRI | select.POLLERR)
            while active.value == 1:
                changes = watchdog.poll(2)
                for change in changes:
                    fileno = change[0]
                    event = change[1]
                    if fileno == tty.fileno():
                        self.env['runtime']['debug'].writeDebugOut('ScreenChange',debug.debugLevel.INFO)                             
                        tty.seek(0)
                        currScreen = str(tty.read()[3:-1])        
                        if currScreen != oldScreen:
                            try:
                                watchdog.unregister(vcsa[ oldScreen ])              
                            except:
                                pass
                            try:
                                watchdog.register(vcsa[ currScreen ], select.POLLPRI | select.POLLERR) 
                            except:
                                pass
                            oldScreen = currScreen
                            try:
                                vcsa[currScreen].seek(0)                        
                                lastScreenContent = vcsa[currScreen].read() 
                            except:
                                pass                             
                            eventQueue.put({"Type":fenrirEventType.ScreenChanged,
                                "Data":self.createScreenEventData(currScreen,lastScreenContent)                            
                            })  
                    else:
                        self.env['runtime']['debug'].writeDebugOut('ScreenUpdate',debug.debugLevel.INFO)                                                 
                        vcsa[currScreen].seek(0)                                                
                        dirtyContent = vcsa[currScreen].read()
                        screenContent = b''
                        timeout = time.time()
                        while screenContent != dirtyContent:
                            screenContent = dirtyContent
                            if time.time() - timeout >= 0.4:
                                break
                            time.sleep(0.02)
                            vcsa[currScreen].seek(0)                             
                            dirtyContent = vcsa[currScreen].read()
                        eventQueue.put({"Type":fenrirEventType.ScreenUpdate,
                            "Data":self.createScreenEventData(currScreen,screenContent)
                        })
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('VCSA:updateWatchdog:' + str(e),debug.debugLevel.ERROR)         
            

    def createScreenEventData(self, screen, content):
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
        encText, encAttr =\
          self.autoDecodeVCSA(content[4:], eventData['lines'], eventData['columns'])
        eventData['text'] = encText
        eventData['attributes'] = encAttr
        return eventData.copy()     
    def updateCharMap(self, screen):
        self.charmap = {}
        try:
            tty = open('/dev/tty' + screen, 'rb')
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('VCSA:updateCharMap:' + str(e),debug.debugLevel.ERROR)   
            return        
        GIO_UNIMAP = 0x4B66
        VT_GETHIFONTMASK = 0x560D
        himask = array("H", (0,))
        ioctl(tty, VT_GETHIFONTMASK, himask)
        self.hichar, = unpack_from("@H", himask)
        sz = 512
        line = ''
        while True:
            try:
                unipairs = array("H", [0]*(2*sz))
                unimapdesc = array("B", pack("@HP", sz, unipairs.buffer_info()[0]))
                ioctl(tty.fileno(), GIO_UNIMAP, unimapdesc)
                break
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('VCSA:updateCharMap:scaling up sz=' + str(sz) + ' ' + str(e),debug.debugLevel.WARNING)   
                sz *= 2
        tty.close()
        ncodes, = unpack_from("@H", unimapdesc)
        utable = unpack_from("@%dH" % (2*ncodes), unipairs)
        for u, b in zip(utable[::2], utable[1::2]):
            if self.charmap.get(b) is None:
                self.charmap[b] = chr(u)

    def autoDecodeVCSA(self, allData, rows, cols):
        allText = ''
        allAttrib = []
        i = 0        
        for y in range(rows):
            lineText = ''
            lineAttrib = []
            for x in range(cols):
                data = allData[i: i + 2]
                i += 2            
                if data == b' \x07':
                    #attr = 7
                    #ink = 7
                    #paper = 0
                    #ch = ' '
                    lineAttrib.append((7,15,0,0,0,0)) # attribute, ink, paper, blink, bold, underline
                    lineText += ' '
                    continue
                (sh,) = unpack("=H", data)
                attr = (sh >> 8) & 0xFF
                ch = sh & 0xFF
                if self.hichar == 0x100:
                    attr >>= 1
                ink = attr & 0x0F
                paper = (attr>>4) & 0x0F
                blink = 0
                #if attr & 1: 
                #    blink = 1
                bold = 0 
                #if attr & 16:
                #    bold = 1
                #if (ink != 7) or (paper != 0):
                #    print(ink,paper)
                if sh & self.hichar:
                    ch |= 0x100
                try:
                    lineText += self.charmap[ch]            
                except KeyError:
                    lineText += '?'
                lineAttrib.append((attr,ink, paper,blink,bold,0)) # attribute, ink, paper, blink, bold, underline
            allText += lineText + '\n'
            allAttrib += lineAttrib
        return str(allText), allAttrib
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
        apps = []
        try:
            currScreen = self.env['screen']['newTTY']
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
                                if self.env['screen']['newApplication'] != i[0]:
                                    self.env['screen']['newApplication'] = i[0]                        
                                return
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)    
        

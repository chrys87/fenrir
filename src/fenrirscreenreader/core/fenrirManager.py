#!/bin/env python3
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import signal, time, argparse, sys

from fenrirscreenreader.core import i18n
from fenrirscreenreader.core import settingsManager
from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType

class fenrirManager():
    def __init__(self):
        self.initialized = False
        cliArgs = self.handleArgs()
        if not cliArgs:
            return
        try:
            self.environment = settingsManager.settingsManager().initFenrirConfig(cliArgs, self)            
            if not self.environment:
                raise RuntimeError('Cannot Initialize. Maybe the configfile is not available or not parseable')
        except RuntimeError:
            raise
        self.environment['runtime']['outputManager'].presentText(_("Start Fenrir"), soundIcon='ScreenReaderOn', interrupt=True)
        signal.signal(signal.SIGINT, self.captureSignal)
        signal.signal(signal.SIGTERM, self.captureSignal)
        self.initialized = True
        self.modifierInput = False
        self.singleKeyCommand = False
        self.command = ''
        self.setProcessName()
    def handleArgs(self):
        args = None
        parser = argparse.ArgumentParser(description="Fenrir Help")
        parser.add_argument('-s', '--setting', metavar='SETTING-FILE', default='/etc/fenrir/settings/settings.conf', help='Use a specified settingsfile')
        parser.add_argument('-o', '--options', metavar='SECTION#SETTING=VALUE;..', default='', help='Overwrite options in given settings file. Sections, settings and Values are cases sensitive')
        parser.add_argument('-d', '--debug',  action='store_true', help='Turns on Debugmode') 
        parser.add_argument('-p', '--print',  action='store_true', help='Print debug messages on screen')
        parser.add_argument('-e', '--emulated-pty',  action='store_true', help='Use PTY emulation and escape sequences for input')
        parser.add_argument('-E', '--emulated-evdev',  action='store_true', help='Use PTY emulation and evdev for input (single instance)')
        try:
            args = parser.parse_args()
        except Exception as e:
            parser.print_help()
        return args    
    def proceed(self):
        if not self.initialized:
            return
        self.environment['runtime']['eventManager'].startMainEventLoop()
        self.shutdown()
    def handleInput(self, event):
        #startTime = time.time()
        self.environment['runtime']['debug'].writeDebugOut('DEBUG INPUT fenrirMan:'  + str(event),debug.debugLevel.INFO)
        if not event['Data']:
            event['Data'] = self.environment['runtime']['inputManager'].getInputEvent()
        if event['Data']:
            event['Data']['EventName'] = self.environment['runtime']['inputManager'].convertEventName(event['Data']['EventName'])
            self.environment['runtime']['inputManager'].handleInputEvent(event['Data'])
        else:
            return

        if self.environment['runtime']['inputManager'].noKeyPressed(): 
            self.environment['runtime']['inputManager'].clearLastDeepInput()
        if self.environment['runtime']['screenManager'].isSuspendingScreen():
            self.environment['runtime']['inputManager'].writeEventBuffer()
        else: 
            if self.environment['runtime']['helpManager'].isTutorialMode():
                self.environment['runtime']['inputManager'].clearEventBuffer()
            if self.environment['runtime']['vmenuManager'].getActive():
                self.environment['runtime']['inputManager'].clearEventBuffer()

            self.detectShortcutCommand()

            if self.modifierInput:
                self.environment['runtime']['inputManager'].clearEventBuffer() 
            if self.singleKeyCommand:
                if self.environment['runtime']['inputManager'].noKeyPressed():
                    self.environment['runtime']['inputManager'].clearEventBuffer() 
            else:
                self.environment['runtime']['inputManager'].writeEventBuffer()
        if self.environment['runtime']['inputManager'].noKeyPressed():
            self.modifierInput = False
            self.singleKeyCommand = False  
        if self.environment['input']['keyForeward'] > 0:
            self.environment['input']['keyForeward'] -=1
        self.environment['runtime']['commandManager'].executeDefaultTrigger('onKeyInput')
        #print('handleInput:',time.time() - startTime)
    def handleByteInput(self, event):
        if not event['Data']:
            return
        if event['Data'] == b'':
            return
        self.environment['runtime']['byteManager'].handleByteInput(event['Data'])
        self.environment['runtime']['commandManager'].executeDefaultTrigger('onByteInput')
    def handleExecuteCommand(self, event):  
        if not event['Data']:
            return          
        if event['Data'] == '':
            return
        command = event['Data']

        # special modes
        if self.environment['runtime']['helpManager'].isTutorialMode():
            if self.environment['runtime']['commandManager'].commandExists( command, 'help'):
                self.environment['runtime']['commandManager'].executeCommand( command, 'help')
                return
        elif self.environment['runtime']['vmenuManager'].getActive():
            if self.environment['runtime']['commandManager'].commandExists( command, 'vmenu-navigation'):
                self.environment['runtime']['commandManager'].executeCommand( command, 'vmenu-navigation')
                return

        # default
        self.environment['runtime']['commandManager'].executeCommand( command, 'commands')            
    def handleRemoteIncomming(self, event):
        if not event['Data']:
            return
        self.environment['runtime']['remoteManager'].handleRemoteIncomming(event['Data'])        
    def handleScreenChange(self, event):
        self.environment['runtime']['screenManager'].hanldeScreenChange(event['Data'])
        '''        
        if self.environment['runtime']['applicationManager'].isApplicationChange():
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onApplicationChange')
            self.environment['runtime']['commandManager'].executeSwitchTrigger('onSwitchApplicationProfile', \
              self.environment['runtime']['applicationManager'].getPrevApplication(), \
              self.environment['runtime']['applicationManager'].getCurrentApplication())          
        '''        
        if self.environment['runtime']['vmenuManager'].getActive():
            return

        self.environment['runtime']['commandManager'].executeDefaultTrigger('onScreenChanged')
        self.environment['runtime']['screenDriver'].getCurrScreen()
    def handleScreenUpdate(self, event):
        #startTime = time.time()
        self.environment['runtime']['screenManager'].handleScreenUpdate(event['Data'])
        '''
        if self.environment['runtime']['applicationManager'].isApplicationChange():
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onApplicationChange')
            self.environment['runtime']['commandManager'].executeSwitchTrigger('onSwitchApplicationProfile', \
              self.environment['runtime']['applicationManager'].getPrevApplication(), \
              self.environment['runtime']['applicationManager'].getCurrentApplication())
        '''
        # timout for the last keypress
        if time.time() - self.environment['runtime']['inputManager'].getLastInputTime() >= 0.3:
            self.environment['runtime']['inputManager'].clearLastDeepInput()
        # has cursor changed?
        if self.environment['runtime']['cursorManager'].isCursorVerticalMove() or \
          self.environment['runtime']['cursorManager'].isCursorHorizontalMove():
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onCursorChange')
        self.environment['runtime']['commandManager'].executeDefaultTrigger('onScreenUpdate')
        self.environment['runtime']['inputManager'].clearLastDeepInput()
        #print('handleScreenUpdate:',time.time() - startTime)
    def handlePlugInputDevice(self, event):
        self.environment['runtime']['inputManager'].handlePlugInputDevice(event['Data'])
        self.environment['runtime']['commandManager'].executeDefaultTrigger('onPlugInputDevice', force=True)
    def handleHeartBeat(self, event):
        self.environment['runtime']['commandManager'].executeDefaultTrigger('onHeartBeat',force=True)  
        #self.environment['runtime']['outputManager'].brailleText(flush=False)


    def detectShortcutCommand(self):    
        if self.environment['input']['keyForeward'] > 0:
            return
        if self.environment['runtime']['inputManager'].isKeyPress():
            self.modifierInput = self.environment['runtime']['inputManager'].currKeyIsModifier()
        else:
            if not self.environment['runtime']['inputManager'].noKeyPressed():
                if self.singleKeyCommand:
                    self.singleKeyCommand = len( self.environment['runtime']['inputManager'].getLastDeepestInput() ) == 1
        # key is already released. we need the old one
        if not( self.singleKeyCommand and self.environment['runtime']['inputManager'].noKeyPressed()):
            shortcut = self.environment['runtime']['inputManager'].getCurrShortcut()                
            self.command = self.environment['runtime']['inputManager'].getCommandForShortcut(shortcut)

        if not self.modifierInput:
            if self.environment['runtime']['inputManager'].isKeyPress():
                if self.command != '':
                    self.singleKeyCommand = True

        if not (self.singleKeyCommand or self.modifierInput):
            return

        # fire event
        if self.command != '':
            if self.modifierInput:
                self.environment['runtime']['eventManager'].putToEventQueue(fenrirEventType.ExecuteCommand, self.command)
                self.command = ''
            else:
                if self.singleKeyCommand:
                    if self.environment['runtime']['inputManager'].noKeyPressed():
                        self.environment['runtime']['eventManager'].putToEventQueue(fenrirEventType.ExecuteCommand, self.command)
                        self.command = ''
    def setProcessName(self, name = 'fenrir'):
        """Attempts to set the process name to 'fenrir'."""

        #sys.argv[0] = name

        # Disabling the import error of setproctitle.
        # pylint: disable-msg=F0401
        try:
            from setproctitle import setproctitle
        except ImportError:
            pass
        else:
            setproctitle(name)
            return True

        try:
            from ctypes import cdll, byref, create_string_buffer
            libc = cdll.LoadLibrary('libc.so.6')
            stringBuffer = create_string_buffer(len(name) + 1)
            stringBuffer.value = bytes(name, 'UTF-8')
            libc.prctl(15, byref(stringBuffer), 0, 0, 0)
            return True
        except:
            pass

        return False
    def shutdownRequest(self):
        try:
            self.environment['runtime']['eventManager'].stopMainEventLoop()
        except:
            pass
    def captureSignal(self, siginit, frame):
        self.shutdownRequest()

    def shutdown(self):
        self.environment['runtime']['eventManager'].stopMainEventLoop()
        self.environment['runtime']['outputManager'].presentText(_("Quit Fenrir"), soundIcon='ScreenReaderOff', interrupt=True)       
        self.environment['runtime']['eventManager'].cleanEventQueue()
        time.sleep(0.6)
        for currManager in self.environment['general']['managerList']:
            if self.environment['runtime'][currManager]:
                self.environment['runtime'][currManager].shutdown()   
                del self.environment['runtime'][currManager]

        self.environment = None


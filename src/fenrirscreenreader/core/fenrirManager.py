#!/bin/env python3
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, sys, signal, time

from fenrirscreenreader.core import i18n
from fenrirscreenreader.core import settingsManager
from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType
import argparse

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
        self.controlMode = True
        self.switchCtrlModeOnce = 0
    def handleArgs(self):
        args = None
        parser = argparse.ArgumentParser(description="Fenrir Help")
        parser.add_argument('-s', '--setting', metavar='SETTING-FILE', default='/etc/fenrir/settings/settings.conf', help='Use a specified settingsfile')
        parser.add_argument('-o', '--options', metavar='SECTION#SETTING=VALUE,..', default='', help='Overwrite options in given settings file')       
        parser.add_argument('-d', '--debug',  action='store_true', help='Turns on Debugmode') 
        parser.add_argument('-p', '--print',  action='store_true', help='Print debug messages on screen')                                         
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
        #startTime = time.time
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

            self.detectCommand()                       

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
        self.environment['runtime']['commandManager'].executeDefaultTrigger('onInput')       
        #print('handleInput:',time.time() - startTime)
    def handleByteInput(self, event):
        if not event['Data']:
            return
        if event['Data'] == b'':
            return
        self.handleControlMode(event['Data'])
        if self.controlMode and not self.switchCtrlModeOnce == 1 or\
          not self.controlMode and self.switchCtrlModeOnce == 1:
            self.detectByteCommand(event['Data'])
    def handleControlMode(self, escapeSequence): 
        if self.switchCtrlModeOnce > 0:
            self.switchCtrlModeOnce -= 1
        if escapeSequence in [b'\x1bR', b'^[R']:
            self.controlMode = not self.controlMode
            self.switchCtrlModeOnce = 0
        if escapeSequence in [b'\x1b:', b'^[:']:
            self.switchCtrlModeOnce = 2
        
    def handleExecuteCommand(self, event):        
        if event['Data'] == '':
            return
        command = event['Data']

        if self.environment['runtime']['helpManager'].isTutorialMode():
            if self.environment['runtime']['commandManager'].commandExists( command, 'help'):
                self.environment['runtime']['commandManager'].executeCommand( command, 'help')
                return
        self.environment['runtime']['commandManager'].executeCommand( command, 'commands')            
    def handleScreenChange(self, event):   
        self.environment['runtime']['screenManager'].hanldeScreenChange(event['Data'])
        '''        
        if self.environment['runtime']['applicationManager'].isApplicationChange():
            self.environment['runtime']['commandManager'].executeDefaultTrigger('onApplicationChange')
            self.environment['runtime']['commandManager'].executeSwitchTrigger('onSwitchApplicationProfile', \
              self.environment['runtime']['applicationManager'].getPrevApplication(), \
              self.environment['runtime']['applicationManager'].getCurrentApplication())          
        '''        
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
        self.environment['runtime']['commandManager'].executeDefaultTrigger('onPlugInputDevice', force=True)   
    
    def handleHeartBeat(self, event):
        self.environment['runtime']['commandManager'].executeDefaultTrigger('onHeartBeat',force=True)  
        #self.environment['runtime']['outputManager'].brailleText(flush=False)                        
    def detectByteCommand(self, escapeSequence):
        command = ''
        try:
            commands = {            
            b'\x1bh':'toggle_tutorial_mode',
            b'\x1b/': 'shut_up',
            b'\x1bO': 'review_bottom',
            b'\x1bU': 'review_top',
            b'\x1bi': 'review_curr_line',
            b'\x1bu': 'review_prev_line',
            b'\x1bo': 'review_next_line',
            b'\x1bJ': 'review_line_begin',
            b'\x1bL': 'review_line_end',
            b'\x1bj': 'review_line_first_char',
            b'\x1bL': 'review_line_last_char',
            b'\x1bk': 'review_curr_word',
            b'\x1bj': 'review_prev_word',
            b'\x1bl': 'review_next_word',
            b'\x1b,': 'review_curr_char',
            b'\x1bm': 'review_prev_char',
            b'\x1b.': 'review_next_char',
            b'\x1b<': 'curr_char_phonetic',
            b'\x1bM': 'prev_char_phonetic',
            b'\x1b>': 'next_char_phonetic',
            b'\x1bOR': 'toggle_sound',
            b'\x1bOS': 'toggle_speech',
            b'\x1b8': 'toggle_highlight_tracking',
            b'\x1bq': 'quit_fenrir',
            b'\x1bt': 'time',
            b'\x1by': 'date',
            b'\x1b[5~': 'prev_clipboard',
            b'\x1b[6~': 'next_clipboard',
            b'\x1bC': 'curr_clipboard',
            b'\x1bc': 'copy_marked_to_clipboard',
            b'\x1bv': 'paste_clipboard',
            b'\x1b[15~': 'import_clipboard_from_file',
            b'\x1bX': 'remove_marks',
            b'\x1bx': 'set_mark',            
            }
            command = commands[escapeSequence].upper()
            self.environment['runtime']['eventManager'].putToEventQueue(fenrirEventType.ExecuteCommand, command)
        except:
            pass    
    def detectCommand(self):    
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
        time.sleep(1)        
        for currManager in self.environment['general']['managerList']:
            if self.environment['runtime'][currManager]:
                self.environment['runtime'][currManager].shutdown()   
                del self.environment['runtime'][currManager]

        self.environment = None


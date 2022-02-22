#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'

    def run(self):
        # enabled? 
        active = self.env['runtime']['settingsManager'].getSettingAsInt('keyboard', 'charEchoMode')
        self.env['runtime']['debug'].writeDebugOut('charEchoMode: ' + str(active) + ' CAPS:' + str(self.env['input']['newCapsLock']),debug.debugLevel.INFO)

        # 0 = off
        if active == 0:
            return
        # 2 = caps only
        if active == 2:
            if not self.env['input']['newCapsLock']:
                return
        # big changes are no char (but the value is bigger than one maybe the differ needs longer than you can type, so a little strange random buffer for now)
        xMove = abs(self.env['screen']['newCursor']['x'] - self.env['screen']['oldCursor']['x'])
        if xMove > 3:
            return
        if self.env['runtime']['inputManager'].getShortcutType() in ['KEY']:
            if self.env['runtime']['inputManager'].getLastDeepestInput() in [['KEY_TAB']]:
                return 
        elif self.env['runtime']['inputManager'].getShortcutType() in ['BYTE']:
            if self.env['runtime']['byteManager'].getLastByteKey() in [b'	', b'\t']:
                return 
        # detect deletion or chilling 
        if self.env['screen']['newCursor']['x'] <= self.env['screen']['oldCursor']['x']:
            return
        # is there any change?
        if not self.env['runtime']['screenManager'].isDelta():
            return
        # filter unneded space on word begin
        currDelta = self.env['screen']['newDelta']
        if len(currDelta.strip()) != len(currDelta) and \
          currDelta.strip() != '':
            currDelta = currDelta.strip()
        self.env['runtime']['outputManager'].presentText(currDelta, interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False)

    def setCallback(self, callback):
        pass


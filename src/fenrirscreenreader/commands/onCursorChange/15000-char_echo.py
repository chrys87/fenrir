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
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'charEcho'):
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
        self.env['runtime']['outputManager'].presentText(currDelta, interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False, reason='char_echo')

    def setCallback(self, callback):
        pass


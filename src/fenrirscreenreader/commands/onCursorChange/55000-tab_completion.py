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
        # try to detect the tab completion by cursor change
        xMove = self.env['screen']['newCursor']['x'] - self.env['screen']['oldCursor']['x']
        if xMove <= 0:
            return
        if self.env['runtime']['inputManager'].getShortcutType() in ['KEY']:
            if not (self.env['runtime']['inputManager'].getLastDeepestInput() in [['KEY_TAB']]):
                if xMove < 5:
                    return 
        elif self.env['runtime']['inputManager'].getShortcutType() in ['BYTE']:
            found = False
            for currByte in self.env['runtime']['byteManager'].getLastByteKey():
                if currByte == 9:
                    found = True
            if not found:
                if xMove < 5:
                    return 
        # is there any change?
        if not self.env['runtime']['screenManager'].isDelta():
            return
        if not xMove == len(self.env['screen']['newDelta']):
            return
        # filter unneded space on word begin
        currDelta = self.env['screen']['newDelta']
        if len(currDelta.strip()) != len(currDelta) and \
          currDelta.strip() != '':
            currDelta = currDelta.strip()
        self.env['runtime']['outputManager'].presentText(currDelta, interrupt=True, announceCapital=True, flush=False)

    def setCallback(self, callback):
        pass


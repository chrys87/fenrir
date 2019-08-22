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
        xMove = abs(self.env['screen']['newCursor']['x'] - self.env['screen']['oldCursor']['x'])
        if xMove == 1:
            return
        # is there any change?
        if not self.env['runtime']['screenManager'].isDelta():
            return            
        if not( (xMove > 1) and xMove == len(self.env['screen']['newDelta'])):
            return                 
        # detect deletion or chilling 
        if self.env['screen']['newCursor']['x'] <= self.env['screen']['oldCursor']['x']:
            return
        
        # filter unneded space on word begin
        currDelta = self.env['screen']['newDelta']
        if len(currDelta.strip()) != len(currDelta) and \
          currDelta.strip() != '':
            currDelta = currDelta.strip()
        self.env['runtime']['outputManager'].presentText(currDelta, interrupt=True, announceCapital=True, flush=False)

    def setCallback(self, callback):
        pass


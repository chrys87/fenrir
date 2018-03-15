#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

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
        if not self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'autoReadIncoming'):
            return
        # is there something to read?
        if not self.env['runtime']['screenManager'].isDelta(ignoreSpace=True):
            return      
        # this must be a keyecho or something      
        #if len(self.env['screen']['newDelta'].strip(' \n\t')) <= 1:
        xMove = abs(self.env['screen']['newCursor']['x'] - self.env['screen']['oldCursor']['x'])
        yMove = abs(self.env['screen']['newCursor']['y'] - self.env['screen']['oldCursor']['y'])
        self.env['runtime']['debug'].writeDebugOut('newX:' + str(self.env['screen']['newCursor']['x']) + 'oldX:' + str(self.env['screen']['oldCursor']['x']),debug.debugLevel.INFO)         
        self.env['runtime']['debug'].writeDebugOut('newY:' + str(self.env['screen']['newCursor']['y']) + 'oldY:' + str(self.env['screen']['oldCursor']['y']),debug.debugLevel.INFO)                 
        self.env['runtime']['debug'].writeDebugOut('xMove:'+ str(xMove)+' yMove:'+str(yMove),debug.debugLevel.INFO)                 
        self.env['runtime']['debug'].writeDebugOut('NewDeltaLen:'+len(self.env['screen']['newDelta']),debug.debugLevel.INFO)                         
        if (xMove >= 1) and xMove == len(self.env['screen']['newDelta']):
        # if len(self.env['screen']['newDelta'].strip(' \n\t0123456789')) <= 2:
            return          
        #if yMove == 1:
        #   if len(self.env['screen']['newDelta'].strip(' \n\t0123456789')) <= 2:
        #    return                        
        self.env['runtime']['outputManager'].presentText(self.env['screen']['newDelta'], interrupt=False, flush=False)

    def setCallback(self, callback):
        pass


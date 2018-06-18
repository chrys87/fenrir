#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import re, string

class barrierManager():
    def __init__(self):
        self.currIsBarrier = False
        self.prefIsBarrier = False
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass  
    def updateBarrierChange(self, isBarrier):  
        self.prefIsBarrier = self.currIsBarrier
        self.currIsBarrier = isBarrier
       
    def resetBarrierChange(self):  
        self.currIsBarrier = False
        self.prefIsBarrier = False
    def isBarrierChange(self):
        return self.currIsBarrier != self.prefIsBarrier
    def handleLineBarrier(self, line, xCursor, output=True, doInterrupt=True):
        isBarrier, sayLine = self.getBarrierText(line, xCursor)
        self.updateBarrierChange(isBarrier)
        #if self.isBarrierChange():
        if isBarrier:
            if output:
                self.env['runtime']['outputManager'].playSoundIcon(soundIcon='BarrierFound', interrupt=doInterrupt)  
        return sayLine               
              
    def hasBarrier(self, start, end):
        # check for corners here
        return True
    def getBarrierText(self, line, xCursor):
        offset = xCursor     
        # is the cursor at the begin or end of an entry:   
        #print(line[:offset + 1].count('│'),line[offset:].count('│'))
        if line[:offset + 1].count('│') > line[offset:].count('│'):
            offset = xCursor - 1
            
        start = line[:offset + 1].rfind('│') + 1
        end = line[offset + 1:].find('│')
        if start == end:
            return False, line
        if start == -1:
            return False, line
        if end == -1:
            return False, line
        else:
            end +=  offset + 1
        if not self.hasBarrier(start, end):
            return False, line
        return True, line[start:end]


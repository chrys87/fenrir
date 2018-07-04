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
              
    def hasBorder(self, text, xCursor, yCursor, validBorder):
        # check for corners here
        lastLineNo = len(text) - 1
        if yCursor <= 0:
            if not (text[0][xCursor] in validBorder):
                return False    
            if len(text) > 1:
                if not (text[1][xCursor] in validBorder):            
                    return False    
            if len(text) > 2:
                if not (text[2][xCursor] in validBorder):            
                    return False                      
        elif yCursor >= lastLineNo:
            if not (text[lastLineNo][xCursor] in validBorder):
                return False    
            if len(text) > 1:
                if not (text[lastLineNo - 1][xCursor] in validBorder):            
                    return False    
            if len(text) > 2:
                if not (text[lastLineNo - 2][xCursor] in validBorder):            
                    return False          
        else:
            if not (text[yCursor][xCursor] in validBorder):
                return False    
            if not (text[yCursor - 1][xCursor] in validBorder):            
                return False    
            if not (text[yCursor + 1][xCursor] in validBorder):            
                return False           
        return True
    def getBarrierText(self, text, xCursor, yCursor):
        line = text[yCursor]
        if not self.env['runtime']['settingsManager'].getSettingAsBool('barrier', 'enabled'):
            return False, line             
        offset = xCursor   

        leftBarriers = self.env['runtime']['settingsManager'].getSetting('barrier', 'barrier')
        rightBarriers = self.env['runtime']['settingsManager'].getSetting('barrier', 'grabDevices')        
        # is the cursor at the begin or end of an entry:   
        #print(line[:offset + 1].count('│'),line[offset:].count('│'))
        # start
        for b in leftBarriers: 
            if line[:offset + 1].count(b) > line[offset:].count(b):
                offset = xCursor - 1
                
            start = line[:offset + 1].rfind(b) + 1
            if start != -1:
                if not self.hasBorder(text, xCursor, yCursor):
                    start = -1                
                break
        if start == -1:
            return False, line                
        # end
        for b in rightBarriers:                 
            end = line[offset + 1:].find(b)
            if end != -1:
                if not self.hasBorder(text, xCursor, yCursor):
                    end = -1
                break
        if end == -1:
            return False, line                            
        if start == end:
            return False, line
        end +=  offset + 1

        return True, line[start:end]


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
    def handleLineBarrier(self, text, xCursor, yCursor, output=True, doInterrupt=True):
        isBarrier = False
        try:
            isBarrier, sayLine = self.getBarrierText(text, xCursor, yCursor)
        except Exception as e:
            return False, ''

        self.updateBarrierChange(isBarrier)
        if self.isBarrierChange():
            if output:        
                if isBarrier:
                    self.env['runtime']['outputManager'].playSoundIcon(soundIcon='BarrierStart', interrupt=doInterrupt)
                else:
                    self.env['runtime']['outputManager'].playSoundIcon(soundIcon='BarrierEnd', interrupt=doInterrupt)
                
        if not isBarrier:
            sayLine = ''   
        return isBarrier, sayLine               
              
    def hasBorder(self, text, xCursor, yCursor, validBorder, barrierPos):
        # check for corners here
        lastLineNo = len(text) - 1
        if yCursor <= 0:
            if not (text[0][barrierPos] in validBorder):
                return False    
            if len(text) > 1:
                if not (text[1][barrierPos] in validBorder):            
                    return False    
            if len(text) > 2:
                if not (text[2][barrierPos] in validBorder):            
                    return False                      
        elif yCursor >= lastLineNo:
            if not (text[lastLineNo][barrierPos] in validBorder):
                return False    
            if len(text) > 1:
                if not (text[lastLineNo - 1][barrierPos] in validBorder):            
                    return False    
            if len(text) > 2:
                if not (text[lastLineNo - 2][barrierPos] in validBorder):            
                    return False          
        else:
            if not (text[yCursor][barrierPos] in validBorder):
                return False    
            if not (text[yCursor - 1][barrierPos] in validBorder):            
                return False    
            if not (text[yCursor + 1][barrierPos] in validBorder):            
                return False  
        return True
    def getBarrierText(self, text, xCursor, yCursor):
        line = text[yCursor]
        if not self.env['runtime']['settingsManager'].getSettingAsBool('barrier', 'enabled'):
            return False, line             
        offset = xCursor   

        leftBarriers = self.env['runtime']['settingsManager'].getSetting('barrier', 'leftBarriers')
        rightBarriers = self.env['runtime']['settingsManager'].getSetting('barrier', 'rightBarriers')        
        # is the cursor at the begin or end of an entry:   
        #print(line[:offset + 1].count('│'),line[offset:].count('│'))
        # start

        for b in leftBarriers: 
            if line[:offset + 1].count(b) > line[offset:].count(b):
                offset = xCursor - 1
            start = line[:offset].rfind(b)
            if start != -1:
                if not self.hasBorder(text, xCursor, yCursor, leftBarriers, start):
                    start = -1  
                else:
                    start += 1  
                break
        if start == -1:
            return False, line                
        # end
        for b in rightBarriers:                 
            end = line[start:].find(b)
            if end != -1:
                end = start + end  
                if not self.hasBorder(text, xCursor, yCursor,rightBarriers, end):
                    end = -1
                break
        if end == -1:
            return False, line                            
        if start == end:
            return False, line

        return True, line[start:end]


#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
#  X   Y Word  END BREAK
# -1, -1, '', True False
def getPrevWord(currX,currY, currText):
    lineBreak = False        
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    x, y, currWord, endOfScreen, lineBreak = getCurrentWord(currX,currY,currText)
    if endOfScreen:
        return x, y, currWord, endOfScreen, lineBreak
    wrappedLines = currText.split('\n') 
    currLine = wrappedLines[y].replace("\t"," ")    
    return x, y, currWord, endOfScreen, lineBreak

def getCurrentWord(currX,currY, currText):
    lineBreak = False    
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    x = currX
    y = currY
    currWord = ''    
    wrappedLines = currText.split('\n')
    currLine = wrappedLines[y].replace("\t"," ")
    return x, y, currWord, endOfScreen, lineBreak

def getNextWord(currX,currY, currText):
    lineBreak = False        
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    x, y, currWord, endOfScreen, lineBreak = getCurrentWord(currX,currY,currText)
    if endOfScreen:
        return x, y, currWord, endOfScreen, lineBreak  
    wrappedLines = currText.split('\n')
    currLine = wrappedLines[y].replace("\t"," ")
    return x, y, currWord, endOfScreen, lineBreak

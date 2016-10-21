#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
#  X   Y Word  END
# -1, -1, '', True
def getPrevWord(currX,currY, currText):
    lineBreak = False        
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen
    x, y, currWord, endOfScreen = getCurrentWord(currX,currY,currText)
    if endOfScreen:
        return x, y, currWord, endOfScreen
    wrappedLines = currText.split('\n') 
    return x, y, currWord, endOfScreen, lineBreak

def getCurrentWord(currX,currY, currText):
    lineBreak = False    
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen
    x = currX
    y = currY
    wrappedLines = currText.split('\n')
    currWord = ''
    currLine = wrappedLines[y].replace("\t"," ")
    return x, y, currWord, endOfScreen, lineBreak

def getNextWord(currX,currY, currText):
    lineBreak = False        
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen
    x = currX
    y = currY
    wrappedLines = currText.split('\n')
    currWord = ''
    currLine = wrappedLines[y].replace("\t"," ")
    return x, y, currWord, endOfScreen, lineBreak

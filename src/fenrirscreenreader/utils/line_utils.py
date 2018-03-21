#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from collections import Counter

def getPrevLine(currX,currY, currText):
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY 
    if y - 1 >= 0:
        y -= 1
    else:
        endOfScreen = True        
    x = 0
    currLine = ''
    if not endOfScreen:
        currLine = wrappedLines[y]                   
    return x, y, currLine, endOfScreen

def getCurrentLine(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY
    x = 0
    currLine = wrappedLines[y]
    return x, y, currLine

def getNextLine(currX,currY, currText):
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY
    if y + 1 < len(wrappedLines):
        y += 1
    else:
        endOfScreen = True
    x = 0
    currLine = ''
    if not endOfScreen:
        currLine = wrappedLines[y]     
    return x, y, currLine, endOfScreen

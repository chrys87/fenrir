#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

def getPrevLine(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY 
    if y - 1 >= 0:
        y -= 1
    x = 0
    currLine = wrappedLines[y]                   
    return x, y, currLine

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
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY
    if y + 1 < len(wrappedLines):
        y += 1
    x = 0
    currLine = wrappedLines[y]    
    return x, y, currLine

def insertNewlines(string, every=64):
    return b'\n'.join(string[i:i+every] for i in range(0, len(string), every))

def splitAtrrLines(string, every=64):
    return list(string[i:i+every] for i in range(0, len(string), every))

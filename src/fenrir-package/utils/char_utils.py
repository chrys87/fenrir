#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

def getPrevChar(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY  
    if x - 1 < 0:
        if y - 1 > 0:
            y -= 1
            x = len(wrappedLines[y]) - 1
    else:
        x -= 1
    currChar = wrappedLines[y][x]        
    return x, y, currChar

def getCurrentChar(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    currChar = wrappedLines[currY][currX]
    return currX, currY, currChar

def getLastCharInLine(currY, currText):
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    currX = len(wrappedLines[currY].rstrip())-1
    if currX < 0:
        currX = 0
    currChar = wrappedLines[currY][currX]
    return currX, currY, currChar

def getNextChar(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY
    if x + 1 == len(wrappedLines[y]):
        if y + 1 < len(wrappedLines) - 1:
            y += 1
            x = 0
    else:
        x += 1    
    currChar = wrappedLines[y][x]            
    return x, y, currChar

def getPhonetic(currChar):
    if len(currChar) != 1:
        return currChar
    phoneticsDict = {
    "A":"alpha", "B":"bravo", "C":"charlie", "D":"delta", "E":"echo",
    "F":"foxtrot", "G":"golf", "H":"hotel", "I":"india", "J":"juliet",
    "K":"kilo", "L":"lima", "M":"mike", "N":"november", "O":"oscar",
    "P":"papa", "Q":"quebec", "R":"romeo", "S":"sierra", "T":"tango",
    "U":"uniform", "V":"victor", "W":"whisky", "X":"x ray",
    "Y":"yankee", "Z":"zulu"
    }
    try:
        return phoneticsDict[currChar.upper()]
    except:
        return currChar

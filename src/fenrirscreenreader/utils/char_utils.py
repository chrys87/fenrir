#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

def getPrevChar(currX,currY, currText):
    lineBreak = False       
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY  
    if x - 1 < 0:
        if y - 1 >= 0:
            y -= 1
            x = len(wrappedLines[y]) - 1
            lineBreak = True
        else:
            lineBreak = False
            endOfScreen = True
    else:
        x -= 1
    currChar = ''
    if not endOfScreen:
        currChar = wrappedLines[y][x]        
    return x, y, currChar, endOfScreen, lineBreak

def getCurrentChar(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    currChar = wrappedLines[currY][currX]
    return currX, currY, currChar

def getUpChar(currX,currY, currText):
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen
    wrappedLines = currText.split('\n')   
    currY -= 1
    if currY < 0:
        currY = 0 
    else:
        endOfScreen = True                
    currChar = ''
    if not endOfScreen:
        currChar = wrappedLines[currY][currX]
    return currX, currY, currChar, endOfScreen

def getDownChar(currX,currY, currText):
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen
    wrappedLines = currText.split('\n')   
    currY += 1
    if currY >= len(wrappedLines):
        currY = len(wrappedLines) -1
    else:
        endOfScreen = True             
    currChar = ''
    if not endOfScreen:
        currChar = wrappedLines[currY][currX]       
    return currX, currY, currChar, endOfScreen

def getLastCharInLine(currY, currText):
    endOfScreen = False    
    if currText == '':
        return -1, -1, ''
    wrappedLines = currText.split('\n')         
    currX = len(wrappedLines[currY].rstrip())-1
    if currX < 0:
        currX = 0
    currChar = wrappedLines[currY][currX]
    return currX, currY, currChar

def getNextChar(currX,currY, currText):
    lineBreak = False        
    endOfScreen = False    
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    wrappedLines = currText.split('\n')         
    x = currX
    y = currY
    if x + 1 == len(wrappedLines[y]):
        if y + 1 <= len(wrappedLines) - 1:
            y += 1
            x = 0
            lineBreak = True
        else:
            lineBreak = False        
            endOfScreen = True
    else:
        x += 1    
    currChar = ''
    if not endOfScreen:
        currChar = wrappedLines[y][x]  

    return x, y, currChar, endOfScreen, lineBreak

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
        phonChar = phoneticsDict[currChar.upper()]
        if currChar.isupper():
            phonChar = phonChar[0].upper() + phonChar[1:]
        return phonChar
    except:
        return currChar
        

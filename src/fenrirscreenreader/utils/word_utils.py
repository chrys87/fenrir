#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import string

def getCurrentWord(currX,currY, currText):
    lineBreak = False    
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    if currText.strip( string.whitespace) == '':
        return currX, currY, '', endOfScreen, lineBreak        
    x = currX
    y = currY
    currWord = ''    
    wrappedLines = currText.split('\n')
    currLine = wrappedLines[y]
    Found = False
    while(not Found):
        if not currLine[x] in string.whitespace:
            if x == 0:
                Found = True
            else:
                if currLine[x - 1] in string.whitespace:
                    Found = True
        if not Found:
            if x - 1 < 0:
                if y - 1 < 0:
                    lineBreak = False
                    endOfScreen = True
                    return currX, currY, '', endOfScreen, lineBreak
                else:
                    y -= 1
                    currLine = wrappedLines[y]
                    x = len( currLine) - 1
                    lineBreak = True
            else:
                x -= 1
    if Found:
        currWord = currLine[x:]
        for d in string.whitespace:
            delimiterPos = currWord.find(d)
            if delimiterPos != -1:
                currWord = currWord[:delimiterPos]               
        return x, y, currWord, endOfScreen, lineBreak
    return currX, currY, '', False, False

def getPrevWord(currX,currY, currText):
    lineBreak = False        
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    if currText.strip( string.whitespace) == '':
        return currX, currY, '', endOfScreen, lineBreak               
    x, y, currWord, endOfScreen, lineBreakCurrWord = getCurrentWord(currX,currY,currText)
    if endOfScreen:
        return x, y, currWord, endOfScreen, lineBreak
    wrappedLines = currText.split('\n')
    currLine = wrappedLines[y]
    if x - 1 < 0:
        if y - 1 < 0:
            lineBreak = False
            endOfScreen = True
            return currX, currY, '', endOfScreen, lineBreak
        else:
            y -= 1
            currLine = wrappedLines[y]
            x = len( currLine) - 1
            lineBreak = True
    else:
        x -= 1
    lineBreakCurrWord = lineBreak or lineBreakCurrWord
    x, y, currWord, endOfScreen, lineBreak = getCurrentWord(x,y,currText)          
    lineBreak = lineBreak or lineBreakCurrWord
    return x, y, currWord, endOfScreen, lineBreak

def getNextWord(currX,currY, currText):
    lineBreak = False    
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    if currText.strip( string.whitespace) == '':
        return currX, currY, '', endOfScreen, lineBreak        
    x = currX
    y = currY
    currWord = ''    
    wrappedLines = currText.split('\n')
    currLine = wrappedLines[y]
    Found = False
    while(not Found):
        if not Found:
            if x + 1 > len( currLine ) - 1:
                if y + 1 > len( wrappedLines ) - 1:
                    lineBreak = False
                    endOfScreen = True
                    return currX, currY, '', endOfScreen, lineBreak
                else:
                    y += 1
                    currLine = wrappedLines[y]
                    x = 0
                    lineBreak = True
            else:
                x += 1
        if not currLine[x] in string.whitespace:
            if x == 0:
                Found = True
            else:
                if currLine[x - 1] in string.whitespace:
                    Found = True                
    if Found:
        currWord = currLine[x:]
        for d in string.whitespace:
            delimiterPos = currWord.find(d)
            if delimiterPos != -1:
                currWord = currWord[:delimiterPos]
        return x, y, currWord, endOfScreen, lineBreak
    return currX, currY, '', False, False
    

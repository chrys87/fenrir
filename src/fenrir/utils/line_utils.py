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

#!/bin/python

def insertNewlines(string, every=64):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

def splitAtrrLines(string, every=64):
    return list(string[i:i+every] for i in range(0, len(string), every))

old = b'das ist ein test'
new = b'das axd ein test'
text = 'das iet ein test'

text = insertNewlines(text,4)
alts = splitAtrrLines(old,4)
neus = splitAtrrLines(new,4)

def trackHighlights(old, new, text):
    result = ''
    text = text.split('\n')
    if len(old) != len(new):
        return result
    if len(text) != len(new):
        return result
    for line in range(len(new)):
        if old[line] != new[line]:
            for column in range(len(new)):
                if old[line][column] != new[line][column]:
                    result += text[line][column]
            result += ' '
    return result

print(trackHighlights(alts,neus,text))    

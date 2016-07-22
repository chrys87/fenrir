#!/bin/python

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

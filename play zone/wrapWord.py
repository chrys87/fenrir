#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

#from core import debug
import string
#  X   Y Word  END BREAK
# -1, -1, '', True False
def getPrevWord(currX,currY, currText):
    lineBreak = False        
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    if currText.strip(string.punctuation +"§ " + string.whitespace) == '':
        return currX, currY, '', endOfScreen, lineBreak               
    x, y, currWord, endOfScreen, lineBreak = getCurrentWord(currX,currY,currText)
    if endOfScreen:
        return x, y, currWord, endOfScreen, lineBreak
    wrappedLines = currText.split('\n')
    currLine = wrappedLines[y]
    Found = False
    while(not Found):
        currWord = 'prev'
        return x, y, currWord, endOfScreen, lineBreak
    return currX, currY, '', False, False

def getCurrentWord(currX,currY, currText):
    lineBreak = False    
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    if currText.strip(string.punctuation +"§ " + string.whitespace) == '':
        return currX, currY, '', endOfScreen, lineBreak        
    x = currX
    y = currY
    currWord = ''    
    wrappedLines = currText.split('\n')
    currLine = wrappedLines[y]
    Found = False
    while(not Found):
        currWord = 'curr'
        return x, y, currWord, endOfScreen, lineBreak
    return currX, currY, '', False, False

def getNextWord(currX,currY, currText):
    lineBreak = False        
    endOfScreen = False
    if currText == '':
        return -1, -1, '', endOfScreen, lineBreak
    if currText.strip(string.punctuation +"§ " + string.whitespace) == '':
        return currX, currY, '', endOfScreen, lineBreak               
    x, y, currWord, endOfScreen, lineBreak = getCurrentWord(currX,currY,currText)
    if endOfScreen:
        return x, y, currWord, endOfScreen, lineBreak  
    wrappedLines = currText.split('\n')
    currLine = wrappedLines[y]
    Found = False
    while(not Found):
        currWord = 'next'
        return x, y, currWord, endOfScreen, lineBreak
    return currX, currY, '', False, False

    

data = """das ist ein test lol
 das ist ein test l 
 das   ist ein  test
                    
 asdf      asdf    a
test            test
  te            test"""
print('__DATA START__')
print(data)
print('__DATA END__\n\n')

x = 0
y = 0
x, y, currWord, endOfScreen, lineBreak = getCurrentWord(x,y,data)
print(x,y,currWord)
    

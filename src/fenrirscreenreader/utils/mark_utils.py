#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

def getTextBetweenMarks(firstMark, secondMark, inText):
    if inText == None:
        return ''
    if not isinstance(inText, list):
        inText = inText.split('\n')
    if len(inText) < 1:
        return ''        
    if firstMark == None:
        return ''
    if secondMark == None:
        return ''        
    if (firstMark['y'] + 1) * (firstMark['x'] + 1) <= (secondMark['y'] + 1) * (secondMark['x'] + 1):
        startMark = firstMark.copy()
        endMark = secondMark.copy()
    else:
        endMark = firstMark.copy()
        startMark = secondMark.copy() 
    textPart = ''
    if startMark['y'] == endMark['y']:
        textPart += inText[startMark['y']][startMark['x']:endMark['x'] + 1]
    else:
        currY = startMark['y']     
        while currY <= endMark['y']:
            if currY < endMark['y']:
                if currY == startMark['y']:
                    textPart += inText[currY][startMark['x']:]
                else:
                    textPart += inText[currY]
                if len(inText[currY].strip()) != 0:
                    if len(textPart) - len(textPart.rstrip()) > 0: 
                        textPart = textPart[:len(textPart.rstrip())] + "\n"
                else:
                    textPart += '\n'
            else:
                textPart += inText[currY][:endMark['x'] + 1]
            currY += 1
    return textPart

def getTextBeforeMark(mark, inText):
    if inText == None:
        return ''
    if mark == None:
        return ''
    return getTextBetweenMarks({'x':0,'y':0}, mark, inText)

def getTextAfterMark(mark, inText):
    if inText == None:
        return ''
    if mark == None:
        return ''
    inText = inText.split('\n')
    return getTextBetweenMarks(mark, {'x':len(inText[0])-1,'y':len(inText)-1}, inText)    

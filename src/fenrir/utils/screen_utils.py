#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from collections import Counter

def insertNewlines(string, every=64):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

def splitOnPos(string, every=64):
    return list(string[i:i+every] for i in range(0, len(string), every))

old = b'eeeemmmeeeeeeeee'
new = b'eeeeeueeeeeeeeee'
text = 'das ist ein test'

def trackHighlights(oldAttr, newAttr, text, lenght):
    result = ''
    currCursor = None
    if oldAttr == newAttr:
        return result,  currCursor
    if len(newAttr) == 0:
        return result,  currCursor
    textLines = insertNewlines(text,lenght)
    textLines = textLines.split('\n')    
    old = splitOnPos(oldAttr,lenght)
    new = splitOnPos(newAttr,lenght)    
    if len(old) != len(new):
        return result,  currCursor
    if len(text) != len(new):
        return result,  currCursor
    try:
        background = Counter(newAttr).most_common(1)
        background = background[0][0]
    except Exception as e:
        background = chr(7)
    for line in range(len(new)):
        if old[line] != new[line]:
            for column in range(len(new)):
                if old[line][column] != new[line][column]:
                    if new[line][column] != background:
                        if not currCursor:
                            currCursor['x'] = column
                            currCursor['y'] = line
                        result += textLines[line][column]
            result += ' '
    return result, currCursor

print(trackHighlights(alts,neus,text))    

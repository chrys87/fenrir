#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from collections import Counter
import string

def removeNonprintable(text):
    # Get the difference of all ASCII characters from the set of printable characters
    nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
    # Use translate to remove all non-printable characters
    return text.translate({ord(character):None for character in nonprintable})

def insertNewlines(string, every=64):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

def splitEvery(toSplit, every=64):
    return list(toSplit[i:i+every] for i in range(0, len(toSplit), every))

def trackHighlights(oldAttr, newAttr, text, lenght):
    result = ''
    currCursor = None
    if oldAttr == newAttr:
        return result,  currCursor
    if len(newAttr) == 0:
        return result,  currCursor
    if len(oldAttr) != len(newAttr):
        return result,  currCursor         
    old = splitEvery(oldAttr,lenght)
    new = splitEvery(newAttr,lenght)      
    textLines = text.split('\n')
    background = []
    print(len(textLines),len(new),new)
    if len(textLines) != len(new):
        return result,  currCursor        
    try:
        bgStat = Counter(newAttr).most_common(3)
        background.append(bgStat[0][0])
        # if there is a third color add a secondary background (for dialogs for example)
        if len(bgStat) > 2:
            if bgStat[1][1] > 40:
                background.append(bgStat[1][0])
    except Exception as e:
        background.append((1,1,1,1))
    print(background)
    for line in range(len(new)):
        if old[line] != new[line]:
            for column in range(len(new[line])):
                print(new[line][column])
                if old[line][column] != new[line][column]:
                    if not new[line][column] in background:
                        if not currCursor:
                            currCursor = {}
                            currCursor['x'] = column
                            currCursor['y'] = line
                        result += textLines[line][column]
            result += ' '
    return result, currCursor 

'''
t = 'hallo\nwelt!'
old = ((1,1,0,0),(1,1,0,0),(1,1,0,0),(1,1,0,0),(1,1,0,0),(1,1,0,0),(1,1,0,0),(1,1,0,0),(1,1,0,0),(1,1,0,0))
new = ((0,1,1,1),(1,1,1,1),(1,1,1,1),(1,1,1,1),(1,1,1,1),(1,1,0,0),(1,1,0,0),(1,1,0,0),(1,1,0,0),(1,1,0,0))

trackHighlights(old,new,t,5)
'''

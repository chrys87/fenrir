#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from collections import Counter
import string
from select import select
from select import epoll
import select
import re

def removeNonprintable(text):
    # Get the difference of all ASCII characters from the set of printable characters
    nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
    # Use translate to remove all non-printable characters
    return text.translate({ord(character):None for character in nonprintable})

def insertNewlines(string, every=64):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

def splitEvery(toSplit, every=64):
    return list(toSplit[i:i+every] for i in range(0, len(toSplit), every))

def hasMoreRead(fd):
    r, w, e = select([fd], [], [], 0)
    return (fd in r)

def hasMorePollPri(fd):
    p = epoll()
    p.register(fd, select.POLLPRI | select.POLLERR)
    r = p.poll(0)
    return (fd in r)

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

    if len(textLines) - 1 != len(new):
        return result,  currCursor        
    try:
        bgStat = Counter(newAttr).most_common(3)
        background.append(bgStat[0][0])
        # if there is a third color add a secondary background (for dialogs for example)
        if len(bgStat) > 2:
            if bgStat[1][1] > 40:
                background.append(bgStat[1][0])
    except Exception as e:
        background.append((7,7,0,0,0,0))
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

class headLineManipulation:
    def __init__(self):
        self.regExSingle = re.compile(r'(([^\w\s])\2{5,})')
        self.regExDouble = re.compile(r'([^\w\s]{2,}){5,}')  
    def replaceHeadLines(self, text):
        result = ''
        newText = ''
        lastPos = 0
        for match in self.regExDouble.finditer(text):
            span = match.span()
            newText += text[lastPos:span[0]]
            numberOfChars = len(text[span[0]:span[1]])
            name = text[span[0]:span[1]][:2]
            if name.strip(name[0]) == '':
                newText += ' ' + str(numberOfChars) + ' ' + name[0] + ' '
            else:
                newText += ' ' + str(int(numberOfChars / 2)) + ' ' + name + ' '
            lastPos = span[1]
        newText += ' ' + text[lastPos:]
        lastPos = 0     
        for match in self.regExSingle.finditer(newText):
            span = match.span()         
            result += text[lastPos:span[0]]
            numberOfChars = len(newText[span[0]:span[1]])
            name = newText[span[0]:span[1]][:2]
            if name.strip(name[0]) == '':               
                result += ' ' + str(numberOfChars) + ' ' + name[0] + ' '
            else:
                result += ' ' + str(int(numberOfChars / 2)) + ' ' + name + ' '        
            lastPos = span[1]
        result += ' ' + newText[lastPos:]
        return result 


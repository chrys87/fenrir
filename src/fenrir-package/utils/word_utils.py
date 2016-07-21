#!/bin/python

def getPrevWord(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    x, y, word = getCurrentWord(currX,currY,currText)
    wrappedLines = currText.split('\n') 
    if (word == ''):
        return currX, currY, '' 
    while True:
        if x < 2:
            if y != 0:
                y -= 1
            else:
                 return currX, currY, '' 
            x = len(wrappedLines[y]) - 1
        else:
            x -= 1
        if wrappedLines[y] != '':
            break
    x, y, word = getCurrentWord(x, y, currText)
    if word == '':
        return currX, currY, ''
    return x, y, word

def getCurrentWord(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    x = currX
    y = currY
    wrappedLines = currText.split('\n')
    wordFound = False
    currWord = ''
    currLine = wrappedLines[y].replace("\t"," ")
    if currLine[x] == ' ' and  x > 1:
        x = x - 2
    while not wordFound:
        x = currLine[:x].rfind(" ")
        if x == -1:
            x = 0
        else:
            x += 1
        wordEnd = currLine[x + 1:].find(" ")
        if wordEnd == -1:
            wordEnd = len(currLine)
        else:
            wordEnd += x + 1
        currWord = currLine[x:wordEnd]
        wordFound = currWord.strip(" \t\n") != ''
        if wordFound:
            break
        if x == 0:
            if y != 0:
                y -= 1
                currLine = wrappedLines[y].replace("\t"," ")
            else:
                 return currX, currY, '' 
            x = len(wrappedLines[y]) - 1
        else:
            x -= 1
    return x, y, currWord

currText = "    das ist ein   test\ntest das\ntesttest\n\ntest"
currY = 4
currX = 3
currX, currY, word = getCurrentWord(currX,currY,currText)
#currX, currY, word = getPrevWord(currX,currY,currText)
print(currX, currY, word)

#!/bin/python

def getPrevWord(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    x, y, word = getCurrentWord(currX,currY,currText)
    if (x == currX) or (y == currY) and (word == ''):
        return currX, currY, '' 
    return getCurrentWord(x - 2, y, currText)

def getCurrentWord(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    x = currX
    y = currY
    wrappedLines = currText.split('\n')
    wordFound = False
    currWord = ''
    if x < 0:
        if y != 0:
            y -= 1
            currLine = wrappedLines[y].replace("\t"," ")
        else:
             return currX, currY, '' 
        x = len(currLine) - 1
    else:
        currLine = wrappedLines[y].replace("\t"," ")
    while not wordFound:
        x = currLine[:x].rfind(" ")
        if x == -1:
            x = 0
        else:
            x += 1
        wordEnd = currLine[x + 2:].find(" ")
        if wordEnd == -1:
            wordEnd = len(currLine[x:])
        else:
            wordEnd += x + 1
        currWord = currLine[x:wordEnd]
        wordFound = currWord.strip(" \t\n") != ''
        print(currWord)		
        if wordFound:
            break
        print(currWord)
        if x == 0:
            if y != 0:
                y -= 1
                currLine = wrappedLines[y].replace("\t"," ")
            else:
                 return currX, currY, '' 
            x = len(currLine) - 1
        else:
            x -= 1
    print(currWord)
    return x, y, currWord

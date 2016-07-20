#!/bin/python

def getCurrentWord(x,y, currText):
    wordFound = False
    currWord = ''
    currLine = wrappedLines[y].replace("\t"," ")
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
                break
            x = len(wrappedLines[y]) - 1
        else:
            x -= 1
    return x, y, currWord    

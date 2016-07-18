#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = environment['screenData']['newCursorReview']
        if environment['screenData']['newCursorReview']['y'] == -1:
            environment['screenData']['newCursorReview'] = environment['screenData']['newCursor'].copy()
        wrappedLines = environment['screenData']['newContentText'].split('\n')
        currWord = ''
        currY = environment['screenData']['newCursorReview']['y']
        currX = environment['screenData']['newCursorReview']['x']        
        wordFound = False
        while not wordFound:
            currLine = wrappedLines[currY].replace("\t"," ")
            currX = currLine[:currX + 1].rfind(" ") + 1
            if currX == -1:
                currX = 0
            wordEnd = currLine[currX + 1:].find(" ") + currX + 1
            if wordEnd == -1:
                wordEnd = len(currLine) -1
            currWord = currLine[currX:wordEnd]
            wordFound = currWord.strip(" \t\n") != ''
            if not wordFound:
                if currX == 0:
                    if currY != 0:
                        currY -= 1
                    else:
                        break
                    currX = len(wrappedLines[currY]) - 1
                else:
                    currX -= 1                             
        environment['screenData']['newCursorReview']['y'] = currY
        environment['screenData']['newCursorReview']['x'] = currX   
                            
        if not wordFound:
            environment['runtime']['outputManager'].presentText(environment, "blank")
        else:
            environment['runtime']['outputManager'].presentText(environment, currWord)
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

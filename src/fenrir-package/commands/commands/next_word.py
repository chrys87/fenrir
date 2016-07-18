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
        currLine = wrappedLines[currY].replace("\t"," ")        
        while not wordFound:
            print(currX)
            currX = currLine[currX:].find(" ") + currX
            print(currX)
            if currX == - 1:
                if currY < environment['screenData']['lines']:
                    currY += 1
                    currLine = wrappedLines[currY].replace("\t"," ")
                    print('erhöhung')
                else:
                    break
                currX = 0   
                print('hmm')    
            print(currX)       
            wordEnd = currLine[currX + 1:].find(" ")
            print(currX)            
            if wordEnd == -1:
                wordEnd = len(currLine)
            else:
                wordEnd += currX + 2
            print(currX)                
            currWord = currLine[currX:wordEnd]
            print(currX)            
            print(currWord)
            wordFound = currWord.strip(" \t\n") != ''
            print(wordFound)
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

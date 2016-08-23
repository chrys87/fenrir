#!/bin/python

def getTextBetweenMarks(firstMark, secondMark, inText):
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
    startX = startMark['x']
    startY = startMark['y']
    textPart = ''
    while startY <= endMark['y']:
        if startY < endMark['y']:
            textPart += inText[startY][startX:]
            if len(textPart) - len(textPart[::-1].strip()) > 0: 
                textPart = textPart[:len(textPart[::-1].strip())] + "\n"
        else:
            textPart += inText[startY][:startX + 1]
        startX = 0
        startY += 1
    return textPart

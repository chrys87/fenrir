#!/bin/python

def getTextBetweenMarks(firstMark, secondMark, inText):
    if inText == None:
        return ''
    if isinstance(inText, list):
        inText = inText.split('\n')
    if len(inText) < 1:
        return ''        
    if inText == '':
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
    currX = startMark['x']
    currY = startMark['y']
    textPart = ''
    while currY <= endMark['y'] and currY <= len(inText):
        if startMark['y'] == endMark['y']:
            textPart += inText[currY][currX:endMark['x'] + 1]
        else:
            if currY < endMark['y']:
                textPart += inText[currY][currX:]
                if len(textPart) - len(textPart[::-1].strip()) > 0: 
                    textPart = textPart[:len(textPart[::-1].strip())] + "\n"
            else:
                textPart += inText[currY][:currX + 1]
        currX = 0
        currY += 1
    return textPart

def getTextBeforeMark(mark, inText):
    if inText == None:
        return ''
    if isinstance(inText, list):
        inText = inText.split('\n')
    if len(inText) < 1:
        return ''        
    if mark == None:
        return ''
    return getTextBetweenMarks({'x':0,'y':0}, mark, inText)

def getTextAfterMark(mark, inText):
    if inText == None:
        return ''
    if isinstance(inText, list):
        inText = inText.split('\n')
    if len(inText) < 1:
        return ''
    if mark == None:
        return ''
    return getTextBetweenMarks(mark, {'x':len(inText[0])-1,'y':len(inText)-1}, inText)    

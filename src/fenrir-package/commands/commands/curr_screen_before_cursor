#!/bin/python

from utils import mark_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        # Prefer review cursor over text cursor
        if (environment['screenData']['newCursorReview'] != None) 
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()

        textBeforeCursor = mark_utils.getTextBeforeMark(cursorPos, environment['screenData']['newContentText'])

        if textBeforeCursor.strip() == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", soundIcon='EmptyLine', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, textBeforeCursor, interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

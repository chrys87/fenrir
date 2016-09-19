#!/bin/python

from utils import mark_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'Reads from the top of the screen to the cursor position'        

    def run(self, environment):
        # Prefer review cursor over text cursor
        if (environment['screenData']['newCursorReview'] != None):
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()

        textBeforeCursor = mark_utils.getTextBeforeMark(cursorPos, environment['screenData']['newContentText'])

        if textBeforeCursor.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", soundIcon='EmptyLine', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, textBeforeCursor, interrupt=True)
   
    def setCallback(self, callback):
        pass


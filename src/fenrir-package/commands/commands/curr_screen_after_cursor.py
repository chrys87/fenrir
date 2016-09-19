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
        return 'reads from the cursor to the bottom of the screen'        

    def run(self, environment):
        # Prefer review cursor over text cursor
        if (environment['screenData']['newCursorReview'] != None):
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()

        textAfterCursor = mark_utils.getTextAfterMark(cursorPos, environment['screenData']['newContentText'])

        if textAfterCursor.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", soundIcon='EmptyLine', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, textAfterCursor, interrupt=True)

    def setCallback(self, callback):
        pass

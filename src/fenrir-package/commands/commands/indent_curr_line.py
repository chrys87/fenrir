#!/bin/python
from utils import line_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        # Prefer review cursor over text cursor

        if (environment['screenData']['newCursorReview'] != None):
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()
        x, y, currLine = \
          line_utils.getCurrentLine(cursorPos['x'], cursorPos['y'], environment['screenData']['newContentText'])
        
        if currLine.strip() == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", soundIcon='EmptyLine', interrupt=True)
        else:        
            environment['runtime']['outputManager'].presentText(environment, "indent "+  str(len(currLine) - len(currLine.lstrip())), interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

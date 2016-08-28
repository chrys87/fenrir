#!/bin/python


class command():
    def __init__(self):
        pass
    def run(self, environment):
        # Prefer review cursor over text cursor

        if (environment['screenData']['newCursorReview'] != None):
            cursorPos = environment['screenData']['newCursorReview'].copy()
        else:
            cursorPos = environment['screenData']['newCursor'].copy()

        environment['runtime']['outputManager'].presentText(environment, "line "+  str(cursorPos['y']+1) + " column "+  str(cursorPos['x']+1), interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

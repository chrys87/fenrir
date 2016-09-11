#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['newCursorReview'] = {'x':0,'y':environment[screenData][lines]}

        environment['runtime']['outputManager'].presentText(environment, "Bottom", interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

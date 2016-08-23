#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = None
        environment['screenData']['newCursorReview'] = None
        environment['runtime']['outputManager'].presentText(environment, "leve review mode", interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

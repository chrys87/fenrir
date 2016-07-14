#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = {'x':-1,'y':-1}
        environment['screenData']['newCursorReview'] = {'x':-1,'y':-1}
        environment['runtime']['outputManager'].speakText(environment, "leve review mode")
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

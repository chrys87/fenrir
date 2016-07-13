#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['runtime']['speechDriver'].cancel()
        environment['screenData']['oldCursorReview'] = {'x':-1,'y':-1}
        environment['screenData']['newCursorReview'] = {'x':-1,'y':-1}
        environment['runtime']['speechDriver'].speak("leve review mode")
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

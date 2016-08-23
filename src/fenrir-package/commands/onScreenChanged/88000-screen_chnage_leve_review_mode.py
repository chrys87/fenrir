#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newTTY'] == environment['screenData']['oldTTY']:
            return environment
        environment['screenData']['oldCursorReview'] = None
        environment['screenData']['newCursorReview'] = None
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

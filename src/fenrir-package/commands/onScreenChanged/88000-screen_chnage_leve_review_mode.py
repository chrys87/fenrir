#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass 
    def getDescription(self, environment):
        return ''        

    def run(self, environment):
        if environment['screenData']['newTTY'] == environment['screenData']['oldTTY']:
            return
        environment['screenData']['oldCursorReview'] = None
        environment['screenData']['newCursorReview'] = None

    def setCallback(self, callback):
        pass

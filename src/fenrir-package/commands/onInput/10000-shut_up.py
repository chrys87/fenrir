#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newDelta'] != environment['screenData']['oldDelta']:
            environment['runtime']['outputManager'].interruptOutput(environment)
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

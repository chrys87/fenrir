#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newDelta'] != environment['screenData']['oldDelta'] or \
          environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            environment['runtime']['speechDriver'].speak(environment['screenData']['newDelta'])
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

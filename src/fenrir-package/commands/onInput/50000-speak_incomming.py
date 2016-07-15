#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        return environment
        if environment['screenData']['newCursor'] != environment['screenData']['oldCursor']:
            print(environment['screenData']['newCursor'] != environment['screenData']['oldCursor'])
            return environment
        if environment['screenData']['newDelta'] != environment['screenData']['oldDelta'] or \
          environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            environment['runtime']['outputManager'].speakText(environment, environment['screenData']['newDelta'], Interrupt=False)
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

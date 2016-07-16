#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newCursor'] == environment['screenData']['oldCursor'] and\
          environment['screenData']['newDelta'] == environment['screenData']['oldDelta']:
            return environment
        environment['runtime']['outputManager'].interruptOutput(environment)
        print('10000-shut_up.py')
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

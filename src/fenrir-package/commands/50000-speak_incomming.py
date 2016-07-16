#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newDelta'] == environment['screenData']['oldDelta'] and 
          environment['screenData']['newTTY'] == environment['screenData']['oldTTY']:
            return environment
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], Interrupt=False)
        print('50000-speak_incomming.py')
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

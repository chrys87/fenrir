#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:    
            environment['runtime']['speechDriver'].cancel()
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

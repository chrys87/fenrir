#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        print('fire')
        #print(environment['screenData']['newContentText'])i
        print(environment['screenData']['newCursor']['x'])
        environment['runtime']['speechDriver'].speak(environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['x']-1])
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

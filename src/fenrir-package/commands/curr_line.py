#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        print('fire')
        #print(environment)
        environment['runtime']['speechDriver'].cancel()
        if environment['screenData']['newContentText'].replace(" ","") == '':
            environment['runtime']['speechDriver'].speak("empty screen")
        else:
            print(environment['screenData']['newCursor'])
            print(environment['screenData']['newContentText'].split('\n'))
            environment['runtime']['speechDriver'].speak(environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']])
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

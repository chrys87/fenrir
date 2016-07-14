#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = environment['screenData']['newCursorReview']
        if environment['screenData']['newCursorReview']['y'] == -1:
            environment['screenData']['newCursorReview'] = environment['screenData']['newCursor'].copy()
        if environment['screenData']['newCursorReview']['y'] - 1 >= 0:
            environment['screenData']['newCursorReview']['y'] = environment['screenData']['newCursorReview']['y'] - 1
                 
        if environment['screenData']['newContentText'].replace(" ","") == '':
            environment['runtime']['outputManager'].speakText(environment, "empty line")
        else:
            environment['runtime']['outputManager'].speakText(environment, environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursorReview']['y']])
        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

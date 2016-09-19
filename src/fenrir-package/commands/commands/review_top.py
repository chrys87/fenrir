#!/bin/python
from utils import char_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'move review to top of screen'        

    def run(self, environment):
        environment['screenData']['newCursorReview'] = {'x':0,'y':0}
        environment['runtime']['outputManager'].presentText(environment, "Top", interrupt=True)

    def setCallback(self, callback):
        pass

#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return ''        

    def run(self, environment):
        if environment['screenData']['newTTY'] == environment['screenData']['oldTTY']:
            return
        environment['runtime']['outputManager'].presentText(environment, "screen " + str(environment['screenData']['newTTY']),soundIcon='ChangeTTY', interrupt=True)         
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=False)

    def setCallback(self, callback):
        pass


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
        environment['commandBuffer']['Marks']['1']  = None
        environment['commandBuffer']['Marks']['2']  = None

    def setCallback(self, callback):
        pass


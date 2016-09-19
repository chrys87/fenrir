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
        return 'displays the last received text'        
    
    def run(self, environment):
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=True)
  
    def setCallback(self, callback):
        pass

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
        return 'reads the contents of the current screen'        

    def run(self, environment):
        if environment['screenData']['newContentText'].strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "screen is empty", soundIcon='EmptyLine', interrupt=True)
        else:    
           environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newContentText'],interrupt=True)
 
    def setCallback(self, callback):
        pass

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
        # TTY Change
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return
        if environment['runtime']['inputManager'].noKeyPressed(environment):
            return            
        # detect an change on the screen, we just want to cursor arround, so no change should appear
        if environment['screenData']['newDelta'] != '':
            return
        if environment['screenData']['newNegativeDelta'] != '':
            return            
        # is it a horizontal change?
        if environment['screenData']['newCursor']['y'] != environment['screenData']['oldCursor']['y'] or\
          environment['screenData']['newCursor']['x'] == environment['screenData']['oldCursor']['x']:
            return
        currChar = environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']][environment['screenData']['newCursor']['x']]
        if not currChar.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, currChar, interrupt=True)
 
    def setCallback(self, callback):
        pass


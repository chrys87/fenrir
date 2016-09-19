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
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'autoReadIncomming'):
            return
        # is there something to read?
        if environment['screenData']['newDelta'] == '':
            return            
        # dont read TTY change
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return
        # its a cursor movement (experimental) - maybe also check current shortcut string?
        if abs(environment['screenData']['newCursor']['x'] - environment['screenData']['oldCursor']['x']) >= 1:
            if len(environment['screenData']['newDelta']) <= 5:
                return          
    
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newDelta'], interrupt=False)

    def setCallback(self, callback):
        pass


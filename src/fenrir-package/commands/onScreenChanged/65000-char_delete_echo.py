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
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'charDeleteEcho'):
            return
   
        # detect typing or chilling
        if environment['screenData']['newCursor']['x'] >= environment['screenData']['oldCursor']['x']:
            return 

        # TTY change
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return

        # More than just a deletion happend
        if environment['screenData']['newDelta'].strip() != '':
            if environment['screenData']['newDelta'] != environment['screenData']['oldDelta']:
    	        return
            
        # No deletion 
        if environment['screenData']['newNegativeDelta'] == '':
            return
        # too much for a single backspace...
        if len(environment['screenData']['newNegativeDelta']) >= 5:
            return           
        environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newNegativeDelta'], interrupt=True)

    def setCallback(self, callback):
        pass


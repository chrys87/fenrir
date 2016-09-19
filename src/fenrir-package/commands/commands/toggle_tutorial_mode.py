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
        environment['generalInformation']['tutorialMode'] = False
        return 'You are leving the tutorial mode. Press that shortcut again to enter the tutorial mode again.'        
    
    def run(self, environment):
        text = 'you entered the tutorial mode. In that mode the commands are not executed. but you get an description what the shortcut does. to leve the tutorial mode press that shortcut again.'
        environment['runtime']['outputManager'].presentText(environment, text,  interrupt=True)                  
        environment['generalInformation']['tutorialMode'] = True            
    
    def setCallback(self, callback):
        pass

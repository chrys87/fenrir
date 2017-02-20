#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        self.env['generalInformation']['tutorialMode'] = False
        return _('You are leaving the tutorial mode. Press that shortcut again to enter the tutorial mode again.')
    
    def run(self):
        text = _('you entered the tutorial mode. In that mode the commands are not executed. but you get a description of what the shortcut does. To leave the tutorial mode, press that shortcut again.')
        self.env['runtime']['outputManager'].presentText(text,  interrupt=True)                  
        self.env['generalInformation']['tutorialMode'] = True            
    
    def setCallback(self, callback):
        pass

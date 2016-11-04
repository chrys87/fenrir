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
        return ''        
    
    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('focus', 'cursor'):
            return    
        if self.env['runtime']['inputManager'].noKeyPressed():
            return     
        if self.env['screenData']['newTTY'] != self.env['screenData']['oldTTY']:
            return
        if self.env['screenData']['newDelta'] != self.env['screenData']['oldDelta']:
            return    
        if self.env['screenData']['newCursor']['y'] == self.env['screenData']['oldCursor']['y']:
            return
        if self.env['runtime']['inputManager'].noKeyPressed():
            return              
        currLine = self.env['screenData']['newContentText'].split('\n')[self.env['screenData']['newCursor']['y']]
        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(currLine, interrupt=True)
 
    def setCallback(self, callback):
        pass


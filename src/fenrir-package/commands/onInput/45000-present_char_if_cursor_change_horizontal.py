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
        currChar = self.env['screenData']['newContentText'].split('\n')[self.env['screenData']['newCursor']['y']][self.env['screenData']['newCursor']['x']] 
        if self.env['screenData']['newTTY'] != self.env['screenData']['oldTTY']:
            return            
        #if self.env['runtime']['inputManager'].noKeyPressed():
        #    return            
        # detect an change on the screen, we just want to cursor arround, so no change should appear
        if self.env['screenData']['newDelta'] != '':
            print('0',currChar )
            return
        if self.env['screenData']['newNegativeDelta'] != '':
            print('1',currChar)
            return            
        # is it a horizontal change?
        if self.env['screenData']['newCursor']['y'] != self.env['screenData']['oldCursor']['y'] or\
          self.env['screenData']['newCursor']['x'] == self.env['screenData']['oldCursor']['x']:
            print('2',currChar, self.env['screenData']['newCursor']['x'],self.env['screenData']['oldCursor']['x'],self.env['screenData']['newCursor']['y'] , self.env['screenData']['oldCursor']['y'])
            return
        currChar = self.env['screenData']['newContentText'].split('\n')[self.env['screenData']['newCursor']['y']][self.env['screenData']['newCursor']['x']]
        if not currChar.strip(" \t\n") == '':
            self.env['runtime']['outputManager'].presentText(currChar, interrupt=True, ignorePunctuation=True)
        print(currChar)
    def setCallback(self, callback):
        pass


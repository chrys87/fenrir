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
        if self.env['runtime']['inputManager'].noKeyPressed():
            return     
        if self.env['runtime']['screenManager'].isScreenChange():
            return
        if self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return
        if len(self.env['input']['currInput']) != 1:              
            return
        if not self.env['input']['currInput'][0] in ['KEY_UP','KEY_DOWN']:              
            return            
        prevLine = self.env['screenData']['oldContentText'].split('\n')[self.env['screenData']['newCursor']['y']]
        currLine = self.env['screenData']['newContentText'].split('\n')[self.env['screenData']['newCursor']['y']]
        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            currPrompt = currLine.find('$')
            rootPrompt = currLine.find('#')
            if currPrompt <= 0:
                if rootPrompt > 0:
                    currPrompt = rootPrompt
                else:
                    announce = currLine            
            if currPrompt > 0:
                remove_digits = str.maketrans('0123456789', '          ')
                if prevLine[:currPrompt].translate(remove_digits) == currLine[:currPrompt].translate(remove_digits):
                    announce = currLine[currPrompt+1:]
                else:
                    announce = currLine                      

        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:            
            self.env['runtime']['outputManager'].presentText(announce, interrupt=True)
        self.env['commandsIgnore']['onScreenUpdate']['INCOMING_IGNORE'] = True
    def setCallback(self, callback):
        pass


#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import word_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'     

    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'wordEcho'):
            return

        # just when cursor move worddetection is needed
        if self.env['screenData']['newCursor']['x'] == self.env['screenData']['oldCursor']['x']:
            return 
        if self.env['runtime']['inputManager'].noKeyPressed():
            return  
        # for now no new line
        if self.env['screenData']['newCursor']['y'] != self.env['screenData']['oldCursor']['y']:
            return 
        if len(self.env['screenData']['newDelta']) > 1:
            return          
 
        # first place could not be the end of a word
        if self.env['screenData']['newCursor']['x'] == 0:
            return

        # get the word
        newContent = self.env['screenData']['newContentText'].split('\n')[self.env['screenData']['newCursor']['y']]
        x, y, currWord =  word_utils.getCurrentWord(self.env['screenData']['newCursor']['x'], 0, newContent)                  
        # was this a typed word?
        if self.env['screenData']['newDelta'] != '':
            if not(newContent[self.env['screenData']['oldCursor']['x']].strip(" \t\n") == '' and x != self.env['screenData']['oldCursor']['x']):
                return
        else:
        # or just arrow arround?
            if not(newContent[self.env['screenData']['newCursor']['x']].strip(" \t\n") == '' and x != self.env['screenData']['newCursor']['x']):
                return            

        if currWord != '':
            self.env['runtime']['outputManager'].presentText(currWord, interrupt=True)

    def setCallback(self, callback):
        pass


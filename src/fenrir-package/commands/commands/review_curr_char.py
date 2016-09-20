#!/bin/python
from utils import char_utils
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
        return 'presents the current character.'        
    
    def run(self, environment):
        environment['screenData']['oldCursorReview'] = environment['screenData']['newCursorReview']
        if environment['screenData']['newCursorReview'] == None:
            environment['screenData']['newCursorReview'] = environment['screenData']['newCursor'].copy()

        environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], currChar = \
          char_utils.getCurrentChar(environment['screenData']['newCursorReview']['x'], environment['screenData']['newCursorReview']['y'], environment['screenData']['newContentText'])
        
        if currChar.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank" ,interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, currChar ,interrupt=True)
  
    def setCallback(self, callback):
        pass

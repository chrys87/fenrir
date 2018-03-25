#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import re

class byteManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass
    def unifyEscapeSeq(self, escapeSequence):   
        convertedEscapeSequence = escapeSequence
        if convertedEscapeSequence[0] == 27:
            convertedEscapeSequence = b'^[' + convertedEscapeSequence[1:]  
        return convertedEscapeSequence        

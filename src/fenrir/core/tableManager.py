#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import re

class tableManager():
    def __init__(self):
        self.headLine = ''
        self.defaultSeparators = ['+',';','|',' ']
        self.noOfHeadLineColumns = 0
        self.headColumnSep = ''
        self.rowColumnSep = ''
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass               
            

#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
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
    def resetTableMode(self):
        self.setHeadLine()
    def setHeadColumnSep(self, columnSep = ''):
        self.headColumnSep = columnSep                
        if columnSep == '':
            self.noOfHeadLineColumns = 0        
        else:
            self.counNoOfHeadColumns()
    def counNoOfHeadColumns(self):
        pass
    def searchForHeadColumnSep(self, headLine):
        if ' ' in headLine:
            return ' '
        return ''
    def setRowColumnSep(self, columnSep = ''):
        self.rowColumnSep = columnSep                
        
    def setHeadLine(self, headLine = ''):        
        self.setHeadColumnSep()
        self.setRowColumnSep()                    
        if headLine != '':
            sep = self.searchForHeadColumnSep(headLine)
            if sep != '':
                self.headLine = headLine
                self.setHeadColumnSep(sep)


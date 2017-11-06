#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import re

class headLineManager():
    def __init__(self):
        self.regExSingle = re.compile(r'(([^\w\s])\2{5,})')
        self.regExDouble = re.compile(r'([^\w\s]{2,}){5,}')  
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass              
    def replaceHeadLines(self, text):
        result = ''
        newText = ''
        lastPos = 0
        for match in self.regExDouble.finditer(text):
            span = match.span()
            newText += text[lastPos:span[0]]
            numberOfChars = len(text[span[0]:span[1]])
            name = text[span[0]:span[1]][:2]
            if name.strip(name[0]) == '':
                newText += ' ' + str(numberOfChars) + ' ' + name[0] + ' '
            else:
                newText += ' ' + str(int(numberOfChars / 2)) + ' ' + name + ' '
            lastPos = span[1]
        newText += ' ' + text[lastPos:]
        lastPos = 0     
        for match in self.regExSingle.finditer(newText):
            span = match.span()         
            result += text[lastPos:span[0]]
            numberOfChars = len(newText[span[0]:span[1]])
            name = newText[span[0]:span[1]][:2]
            if name.strip(name[0]) == '':               
                result += ' ' + str(numberOfChars) + ' ' + name[0] + ' '
            else:
                result += ' ' + str(int(numberOfChars / 2)) + ' ' + name + ' '        
            lastPos = span[1]
        result += ' ' + newText[lastPos:]
        return result 

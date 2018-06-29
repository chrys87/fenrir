#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import re, string

class textManager():
    def __init__(self):
        # https://regex101.com/
        self.regExSingle = re.compile(r'(([^\w\s])\2{5,})')
        self.regExDouble = re.compile(r'([^\w\s]{2,}){5,}')  
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass    

    def replaceHeadLines(self, text):
        # fast len check for bigger typing echo
        if len(text) < 5:
            return text
        # more strong check, to not match if not needed:
        if len(text.strip(string.ascii_letters+string.digits+string.whitespace)) < 5:
            return text        
        result = ''
        newText = ''
        lastPos = 0
        for match in self.regExDouble.finditer(text):
            span = match.span()
            newText += text[lastPos:span[0]]
            numberOfChars = len(text[span[0]:span[1]])
            name = text[span[0]:span[1]][:2]
            if not self.env['runtime']['punctuationManager'].isPuctuation(name[0]):  
                lastPos = span[1]
                continue          
            if name[0] == name[1]:
                newText += ' ' + str(numberOfChars) + ' ' + self.env['runtime']['punctuationManager'].proceedPunctuation(name[0], True) + ' '
            else:
                newText += ' ' + str(int(numberOfChars / 2)) + ' ' + self.env['runtime']['punctuationManager'].proceedPunctuation(name, True) + ' '
            lastPos = span[1]
        if lastPos != 0:
            newText += ' '
        newText += text[lastPos:]
        lastPos = 0     
        for match in self.regExSingle.finditer(newText):
            span = match.span()         
            result += text[lastPos:span[0]]
            numberOfChars = len(newText[span[0]:span[1]])
            name = newText[span[0]:span[1]][:2]
            if not self.env['runtime']['punctuationManager'].isPuctuation(name[0]):  
                lastPos = span[1]            
                continue               
            if name[0] == name[1]:
                result += ' ' + str(numberOfChars) + ' ' + self.env['runtime']['punctuationManager'].proceedPunctuation(name[0], True) + ' '
            else:
                result += ' ' + str(int(numberOfChars / 2)) + ' ' + self.env['runtime']['punctuationManager'].proceedPunctuation(name, True) + ' '
            lastPos = span[1]
        if lastPos != 0:
            result += ' '                   
        result += newText[lastPos:]
        return result 

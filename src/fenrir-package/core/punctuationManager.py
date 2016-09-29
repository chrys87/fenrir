#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import string
from core import debug

class punctuationManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.allPunctNone = dict.fromkeys(map(ord, string.punctuation), None)
        self.punctuation = {
        'currLevel':'3',
        'levels':{
          '1':',',
          '2':'.',
          '3':'.,:-$~+*-/\\@',
          },
        'punctuationDict':{
          '&':'and',
          "'":"apostrophe",
          '@':'at',
          '\\':'backslash',
          '|':'bar',
          '!':'bang',
          '^':'carrot',
          ':':'colon',
          ',':'comma',
          '-':'dash',
          '$':'dollar',
          '.':'dot',
          '>':'greater',
          '`':'grave',
          '#':'hash',
          '{':'left brace',
          '[':'left bracket',
          '(':'left paren',
          '<':'less',
          '%':'percent',
          '+':'plus',
          '?':'question',
          '"':'quote',
          ')':'right paren',
          '}':'right brace',
          ']':'right bracket',
          ';':'semicolon',
          '/':'slash',
          '*':'star',
          '~':'tilde',
          '_':'line',
          '=':'equals',
          },
        'customDict':{
          'chrys':'awsome',
          'cool':'mr chrys'
          }          
        }
    def shutdown(self):
        pass
    def removeUnused(self, text):
        return text.translate(self.allPunctNone)   
    
    def useCustomDict(self, text, customDict):
        resultText = str(text)
        if customDict:
            for key,item in customDict.items():
                resultText = resultText.replace(str(key),str(item))
        return resultText
    def usePunctuationDict(self, text, punctuationDict, punctuation):
        resultText = str(text)

        if punctuationDict and punctuation and punctuation != '':
            for key,item in punctuationDict.items():
                if key in punctuation:
                    resultText = resultText.replace(str(key),' ' +str(item) +' ')

        return resultText
    
    def proceedPunctuation(self, text, ignorePunctuation=False):
        resultText = self.useCustomDict(text, self.punctuation['customDict'])
        currPunctLevel = ''
        if not ignorePunctuation and self.punctuation['currLevel'] in self.punctuation['levels']:
            currPunctLevel = self.punctuation['levels'][self.punctuation['currLevel']]
        else:
            currPunctLevel = string.punctuation
        resultText = self.usePunctuationDict(resultText, self.punctuation['punctuationDict'], currPunctLevel)
        resultText = self.removeUnused(resultText)
        return resultText

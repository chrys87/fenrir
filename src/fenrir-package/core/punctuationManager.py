#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class punctuationManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.punctuation = {
        'currLevel':'1',
        'levels':{
          '1':',',
          '2':'.',
          '3':'.,',
          },
        'punctuationDict':{
          '.':'punkt',
          ',':'komma'
          },
        'customDict':{
          'chrys':'awsome',
          'cool':'mr chrys'
          }          
        }
    def shutdown(self):
        pass
    def removeUnused(self, text):
        resultText = text.translate(text.maketrans(string.punctuation, ' '*len(string.punctuation)))   
        return resultText
    def useCustomDict(self, text, customDict):
        resultText = text
        for key,item in customDict.items():
            resultText = resultText.replace(str(key),str(item))
        return resultText
    def usePunctuationDict(self, text, punctuationDict, punctuation):
        resultText = str(text)
        for key,item in punctuationDict.items():
            if key in punctuation:
                resultText = resultText.replace(str(key),' ' +str(item) +' ')
        return resultText
    
    def proceedPunctuation(self, text, ignoreLevel=False):
        resultText = self.useCustomDict(text, self.punctuation['customDict'])
        currPunctLevel = ''
        if not ignoreLevel:
            currPunctLevel = self.punctuation['levels'][self.punctuation['currLevel']]
        else:
            currPunctLevel = string.punctuation
        resultText = self.usePunctuationDict(resultText, self.punctuation['punctuationDict'], currPunctLevel)
        resultText = self.removeUnused(resultText)
        return resultText

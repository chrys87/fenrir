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
        self.allPunctNone = dict.fromkeys(map(ord, string.punctuation), ' ')
        # replace with space: 
        # dot, comma, grave, apostrophe
        for char in [ord('.'),ord(','),ord('`'),ord("'")]:
            self.allPunctNone[char] = None
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
        resultText = self.useCustomDict(text, self.env['punctuation']['CUSTOMDICT'])
        resultText = self.useCustomDict(text, self.env['punctuation']['EMOJDICT'])
        currPunctLevel = ''
        if not ignorePunctuation and self.env['runtime']['settingsManager'].getSetting('general', 'punctuationLevel').lower() in self.env['punctuation']['LEVELDICT']:
            currPunctLevel = self.env['punctuation']['LEVELDICT'][self.env['runtime']['settingsManager'].getSetting('general', 'punctuationLevel').lower()]
        else:
            currPunctLevel = string.punctuation
        resultText = self.usePunctuationDict(resultText, self.env['punctuation']['PUNCTDICT'], currPunctLevel)
        resultText = self.removeUnused(resultText)
        return resultText

    def cyclePunctuation(self):
        punctList = list(self.env['punctuation']['LEVELDICT'].keys())
        try:
            currIndex = punctList.index(self.env['runtime']['settingsManager'].getSetting('general', 'punctuationLevel').lower()) # curr punctuation
        except:
            return False
        currIndex += 1
        if currIndex >= len(punctList):
            currIndex = 0
        currLevel = punctList[currIndex]
        self.env['runtime']['settingsManager'].setSetting('general', 'punctuationLevel', currLevel.lower())
        return True

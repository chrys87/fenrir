#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import string
from fenrirscreenreader.core import debug
import os, inspect, re
currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
fenrirPath = os.path.dirname(currentdir)

class punctuationManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.allPunctNone = dict.fromkeys(map(ord, string.punctuation +"§ "), ' ')
        # replace with None: 
        # dot, comma, grave, apostrophe
        #for char in [ord('`'),ord("'")]:
        #    self.allPunctNone[char] = None
        # dont restore the following (for announce correct pause)
        for char in [ord("'"),ord('.'), ord(','), ord(';'), ord(':'), ord('?'), ord('!'), ord('-')]:
            self.allPunctNone[char] = chr(char)
    def shutdown(self):
        pass
    def removeUnused(self, text, currLevel = ''):
        # dont translate dot and comma because they create a pause
        currAllPunctNone = self.allPunctNone.copy()
        for char in currLevel:
            try:
                del currAllPunctNone[ord(char)]
            except:
                pass
        return text.translate(currAllPunctNone)   
    
    def useCustomDict(self, text, customDict, seperator=''):
        resultText = str(text)
        if customDict:
            for key,item in customDict.items():
                resultText = resultText.replace(str(key),seperator + str(item) + seperator)
        return resultText
    
    def usePunctuationDict(self, text, punctuationDict, punctuation):
        resultText = str(text)

        if punctuationDict and punctuation and punctuation != '':
            if ' ' in punctuation:
                resultText = resultText.replace(' ',' ' + punctuationDict[' '] + ' ')
            for key,item in punctuationDict.items():
                if key in punctuation and key not in ' ':
                    if self.env['runtime']['settingsManager'].getSetting('general', 'respectPunctuationPause') and \
                      len(key) == 1 and \
                      key in "',.;:?!":
                        resultText = resultText.replace(str(key),' ' +str(item) + str(key) + ' ')                    
                    else:
                        resultText = resultText.replace(str(key),' ' +str(item) + ' ')
        return resultText
    def isPuctuation(self, char):
        return char in self.env['punctuation']['PUNCTDICT']
    def proceedPunctuation(self, text, ignorePunctuation=False):
        resultText = text
        resultText = self.useCustomDict(resultText, self.env['punctuation']['CUSTOMDICT'])
        if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'emoticons'):
            resultText = self.useCustomDict(resultText, self.env['punctuation']['EMOTICONDICT'], ' ')
        currPunctLevel = ''
        if not ignorePunctuation and self.env['runtime']['settingsManager'].getSetting('general', 'punctuationLevel').lower() in self.env['punctuation']['LEVELDICT']:
            currPunctLevel = self.env['punctuation']['LEVELDICT'][self.env['runtime']['settingsManager'].getSetting('general', 'punctuationLevel').lower()]
        else:
            currPunctLevel = string.punctuation +' §'
        resultText = self.usePunctuationDict(resultText, self.env['punctuation']['PUNCTDICT'], currPunctLevel)
        resultText = self.removeUnused(resultText, currPunctLevel)
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
    def loadDicts(self, dictConfigPath=fenrirPath + '/../../config/punctuation/default.conf'):
        dictConfig = open(dictConfigPath,"r")
        currDictName = ''
        while(True):
            line = dictConfig.readline()
            if not line:
                break
            line = line.replace('\n','')
            if line.replace(" ","") == '':
                continue
            if line.replace(" ","").startswith("#"):
                continue
            if line.replace(" ","").upper().startswith("[") and \
              line.replace(" ","").upper().endswith("DICT]"):
                currDictName = line[line.find('[') + 1 :line.upper().find('DICT]') + 4].upper()
            else:
                if currDictName == '':
                    continue
                if not ":===:" in line:
                    continue
                sepLine = line.split(':===:')
                if len(sepLine) == 1:
                    sepLine.append('')
                elif len(sepLine) < 1:
                    continue
                elif len(sepLine) > 2:
                    sepLine[1] = ':===:'
                self.env['punctuation'][currDictName][sepLine[0]] = sepLine[1]
                self.env['runtime']['debug'].writeDebugOut("Punctuation: " + currDictName + '.' + str(sepLine[0]) + ' :' + sepLine[1] ,debug.debugLevel.INFO, onAnyLevel=True)    
        dictConfig.close()        

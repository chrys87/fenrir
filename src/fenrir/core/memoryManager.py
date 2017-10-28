#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from core import debug

class inputManager():
    def __init__(self):
        self.listStorage = {}
    def initialize(self, environment):
        self.env = environment
    def addValueList(self, name, value):
        pass
    def addIndexList(self, name, maxLength = None, currList = [], currIndex = 0):
        self.listStorage[name] = {'list': currList, 'index': currIndex, 'maxLength': maxLength}
    def getNextIndexListElement(self, name):
        pass
    def getPrefIndexListElement(self, name):
        pass  
    def getFirstIndexListElement(self, name):
        pass
    def getLastIndexListElement(self, name):
        pass  
    def getCurrentIndex(self,name):
        try:        
            return self.listStorage[name]['list']['index']    
        except:
            retrun 0
    def getIndexListElement(self, name):
        currIndex = self.getCurrentIndex(name)
        try:        
            return self.listStorage[name]['list'][currIndex]
        except:
            return []

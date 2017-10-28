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
    def addValueToFirstIndex(self, name, value):
        pass
    def addIndexList(self, name, maxLength = None, currList = [], currIndex = 0):
        self.listStorage[name] = {'list': currList, 'index': currIndex, 'maxLength': maxLength}
    def getNextIndex(self, name):
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False
        self.listStorage[name]['index'] += 1
        if self.listStorage[name]['index'] > len(self.listStorage[name]['list']) -1:
            self.listStorage[name]['index'] = 0
        return True    
    def setPrefIndex(self, name):
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False
    def setFirstIndex(self, name):
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False
        self.listStorage[name]['index'] = 0
        return True  
    def setLastIndex(self, name):
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False
        self.listStorage[name]['index'] = self.listStorage[name]['list'] -1 
        return True  
    def clearCurrentIndexList(self, name):
        self.listStorage[name]['index'] = []
        self.listStorage[name]['index'] = -1
    def getCurrentIndex(self,name):
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False        
        try:        
            return self.listStorage[name]['index']    
        except:
            retrun -1
    def isIndexListEmpty(self, name):
        return len(self.listStorage[name]['list']) == 0
    def getIndexListElement(self, name):
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False        
        currIndex = self.getCurrentIndex(name)
        if currIndex == -1:
            return None
        try:        
            return self.listStorage[name]['list'][currIndex]
        except:
            return None

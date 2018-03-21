#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import time
from fenrirscreenreader.core import debug

class memoryManager():
    def __init__(self):
        self.listStorage = {}
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def listStorageValid(self,name, checkIndex = False):
        try:
            if checkIndex:
                index = self.listStorage[name]['index']
                if index == -1:
                    return self.listStorage[name]['list'] == []        
                return self.listStorage[name]['list'][index] != None
            else:
                return isinstance(self.listStorage[name]['list'],list)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("listStorageValid " + str(e),debug.debugLevel.ERROR)
        return False                    
    def addValueToFirstIndex(self, name, value):
        if not self.listStorageValid(name):
            return
        if self.listStorage[name]['maxLength'] == None:
            self.listStorage[name]['list'] = [value] + self.listStorage[name]['list']
        else:        
            self.listStorage[name]['list'] = [value] + self.listStorage[name]['list'][:self.listStorage[name]['maxLength'] -1]
        self.listStorage[name]['index'] = 0
    def addIndexList(self, name, maxLength = None, currList = [], currIndex = -1):
        if len(currList) != 0 and (currIndex == -1):
            currIndex = 0
        self.listStorage[name] = {'list': currList, 'index': currIndex, 'maxLength': maxLength}
    def isLastIndex(self, name):
        if not self.listStorageValid(name):
            return False    
        return self.listStorage[name]['index'] == len(self.listStorage[name]['list']) - 1
    def isFirstIndex(self, name):
        if not self.listStorageValid(name):
            return False       
        return self.listStorage[name]['index'] == 0 
    def getNextIndex(self, name):
        if not self.listStorageValid(name):
            return False      
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False
        self.listStorage[name]['index'] += 1
        if self.listStorage[name]['index'] > len(self.listStorage[name]['list']) -1:
            self.listStorage[name]['index'] = 0
        return True    
    def setPrefIndex(self, name):
        if not self.listStorageValid(name):
            return False     
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False
        self.listStorage[name]['index'] -= 1
        if self.listStorage[name]['index'] < 0:
            self.listStorage[name]['index'] = len(self.listStorage[name]['list']) -1
        return True
    def setFirstIndex(self, name):
        if not self.listStorageValid(name):
            return False    
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False
        self.listStorage[name]['index'] = 0
        return True
    def getIndexListLen(self, name):
        if not self.listStorageValid(name):
            return 0      
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return 0          
        return len(self.listStorage[name])
    def setLastIndex(self, name):
        if not self.listStorageValid(name):
            return False      
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False
        self.listStorage[name]['index'] = len(self.listStorage[name]['list']) -1 
        return True  
    def clearCurrentIndexList(self, name):
        if not self.listStorageValid(name):
            return False      
        self.listStorage[name]['index'] = []
        self.listStorage[name]['index'] = -1
    def getCurrentIndex(self,name):
        if not self.listStorageValid(name):
            return False    
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return False        
        try:        
            return self.listStorage[name]['index']    
        except:
            retrun -1
    def isIndexListEmpty(self, name):
        if not self.listStorageValid(name):
            return False      
        return len(self.listStorage[name]['list']) == 0
    def getIndexListElement(self, name):
        if not self.listStorageValid(name):
            return None    
        if self.isIndexListEmpty(name):
            self.listStorage[name]['index'] = -1
            return None        
        currIndex = self.getCurrentIndex(name)
        if currIndex == -1:
            return None
        try:       
            return self.listStorage[name]['list'][currIndex]
        except:
            return None

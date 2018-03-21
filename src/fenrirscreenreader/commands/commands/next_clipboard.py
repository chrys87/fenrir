#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('selects the next clipboard')        
    
    def run(self):
        if self.env['runtime']['memoryManager'].isIndexListEmpty('clipboardHistory'):
            self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
            return      
        self.env['runtime']['memoryManager'].getNextIndex('clipboardHistory')               
        isFirst = self.env['runtime']['memoryManager'].isFirstIndex('clipboardHistory')   
        isLast = self.env['runtime']['memoryManager'].isLastIndex('clipboardHistory')               
        clipboard = self.env['runtime']['memoryManager'].getIndexListElement('clipboardHistory')            
        if isFirst:
            self.env['runtime']['outputManager'].presentText(_('First clipboard '), interrupt=True)   
        if isLast:
            self.env['runtime']['outputManager'].presentText(_('Last clipboard '), interrupt=True)                     
        
        speechInterrupt = not(isLast or isFirst)
        self.env['runtime']['outputManager'].presentText(clipboard, interrupt = speechInterrupt)
             
    def setCallback(self, callback):
        pass

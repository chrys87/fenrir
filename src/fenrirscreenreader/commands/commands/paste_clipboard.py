#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import time

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['memoryManager'].addIndexList('clipboardHistory', self.env['runtime']['settingsManager'].getSettingAsInt('general', 'numberOfClipboards'))
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('pastes the text from the currently selected clipboard')        
    
    def run(self):    
        if self.env['runtime']['memoryManager'].isIndexListEmpty('clipboardHistory'):
            self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
            return                                          
        self.env['runtime']['outputManager'].presentText('paste clipboard', soundIcon='PasteClipboardOnScreen', interrupt=True)
        clipboard = self.env['runtime']['memoryManager'].getIndexListElement('clipboardHistory')
        self.env['runtime']['screenManager'].injectTextToScreen(clipboard)
              
    def setCallback(self, callback):
        pass

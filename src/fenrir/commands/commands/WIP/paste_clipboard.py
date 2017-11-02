#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
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
        currClipboard = self.env['commandBuffer']['currClipboard']
        if currClipboard < 0:
            self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
            return
        if not self.env['commandBuffer']['clipboard']:
            self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
            return
        if not self.env['commandBuffer']['clipboard'][currClipboard]:
            self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
            return 
        if self.env['commandBuffer']['clipboard'][currClipboard] == '':
            self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
            return                                         
        self.env['runtime']['outputManager'].presentText('paste clipboard', soundIcon='PasteClipboardOnScreen', interrupt=True)
        time.sleep(0.01)
        self.env['runtime']['screenManager'].injectTextToScreen(self.env['commandBuffer']['clipboard'][currClipboard])
              
    def setCallback(self, callback):
        pass

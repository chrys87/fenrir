#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import mark_utils
import os

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('imports text from clipboard file to the clipboard')    
    
    def run(self):
        clipboardFilePath = self.env['runtime']['settingsManager'].getSetting('general', 'clipboardExportPath')
        clipboardFilePath = clipboardFilePath.replace('$user',self.env['general']['currUser'])        
        clipboardFilePath = clipboardFilePath.replace('$USER',self.env['general']['currUser'])        
        clipboardFilePath = clipboardFilePath.replace('$User',self.env['general']['currUser'])                        
        if not os.path.exists(clipboardFilePath):
            self.env['runtime']['outputManager'].presentText(_('File does not exist'), soundIcon='', interrupt=True)        
            return
        clipboardFile = open(clipboardFilePath,'r') 
        imported = clipboardFile.read()
        clipboardFile.close()
        self.env['runtime']['memoryManager'].addValueToFirstIndex('clipboardHistory', imported)        

        self.env['runtime']['outputManager'].presentText('Import to Clipboard', soundIcon='CopyToClipboard', interrupt=True)
        self.env['runtime']['outputManager'].presentText(imported, soundIcon='', interrupt=False)        
        

    def setCallback(self, callback):
        pass

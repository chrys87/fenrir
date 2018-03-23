#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import os

class command():
    def __init__(self):
        pass
    def initialize(self, environment, scriptPath=''):
        self.env = environment

    def shutdown(self):
        pass
    def getDescription(self):
        return _('export the current fenrir clipboard to a file')
    def run(self):  
        clipboardFilePath = self.env['runtime']['settingsManager'].getSetting('general', 'clipboardExportPath')
        clipboardFilePath = clipboardFilePath.replace('$user',self.env['general']['currUser'])        
        clipboardFilePath = clipboardFilePath.replace('$USER',self.env['general']['currUser'])        
        clipboardFilePath = clipboardFilePath.replace('$User',self.env['general']['currUser'])                        
        clipboardFile = open(clipboardFilePath,'w')        
        try:
            if self.env['runtime']['memoryManager'].isIndexListEmpty('clipboardHistory'):
                self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
                return 
            clipboard = self.env['runtime']['memoryManager'].getIndexListElement('clipboardHistory')                             
            clipboardFile.write(clipboard)
            clipboardFile.close()
            os.chmod(clipboardFilePath, 0o666)
            self.env['runtime']['outputManager'].presentText(_('clipboard exported to file'), interrupt=True)            
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('export_clipboard_to_file:run: Filepath:'+ clipboardFile +' trace:' + str(e),debug.debugLevel.ERROR)                                
        
    def setCallback(self, callback):
        pass

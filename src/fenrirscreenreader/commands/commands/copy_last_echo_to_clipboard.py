#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import mark_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('copies last presented text to the clipboard')    
    
    def run(self):
        lastEcho = self.env['runtime']['outputManager'].getLastEcho()
        self.env['runtime']['memoryManager'].addValueToFirstIndex('clipboardHistory', lastEcho)
        self.env['runtime']['outputManager'].presentText(lastEcho, soundIcon='CopyToClipboard', interrupt=True)

    def setCallback(self, callback):
        pass

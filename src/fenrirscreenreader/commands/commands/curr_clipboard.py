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
        return _('speaks the contents of the currently selected clipboard')       

    def run(self):
        if self.env['runtime']['memoryManager'].isIndexListEmpty('clipboardHistory'):
            self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
            return 
        clipboard = self.env['runtime']['memoryManager'].getIndexListElement('clipboardHistory')
        self.env['runtime']['outputManager'].presentText(clipboard , interrupt=True)
               
    def setCallback(self, callback):
        pass

#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('reads the contents of the current screen')        

    def run(self):
        if self.env['screenData']['newContentText'].isspace():
            self.env['runtime']['outputManager'].presentText(_("screen is empty"), soundIcon='EmptyLine', interrupt=True)
        else:    
           self.env['runtime']['outputManager'].presentText(self.env['screenData']['newContentText'],interrupt=True)
 
    def setCallback(self, callback):
        pass

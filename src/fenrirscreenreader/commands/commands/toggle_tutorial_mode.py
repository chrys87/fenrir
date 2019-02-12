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
        self.env['runtime']['helpManager'].toggleTutorialMode()
        return _('Exiting tutorial mode. To enter tutorial mode again press Fenrir+f1')
    def run(self):
        self.env['runtime']['helpManager'].toggleTutorialMode()
        if self.env['runtime']['helpManager'].isTutorialMode():
            self.env['runtime']['outputManager'].presentText( _('Entering tutorial mode. In this mode commands are described but not executed. You can move through the list of commands with the up and down arrow keys. To Exit tutorial mode press Fenrir+f1.'),  interrupt=True)                             
    def setCallback(self, callback):
        pass

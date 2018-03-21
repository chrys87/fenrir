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
        return 'No Description found'      

    def run(self):
        self.env['runtime']['outputManager'].presentText(_("screen {0}").format(self.env['screen']['newTTY']),soundIcon='ChangeTTY', interrupt=True, flush=False)         
        self.env['runtime']['outputManager'].presentText(self.env['screen']['newContentText'], interrupt=False, flush=False)

    def setCallback(self, callback):
        pass


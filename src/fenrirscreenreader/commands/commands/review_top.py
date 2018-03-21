#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import char_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('move review to top of screen')        

    def run(self):
        self.env['screen']['newCursorReview'] = {'x':0,'y':0}
        self.env['runtime']['outputManager'].presentText(_("Top"), interrupt=True, flush=False)

    def setCallback(self, callback):
        pass

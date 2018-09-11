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
        return _('Move review to the bottom of the screen')         

    def run(self):
        self.env['screen']['newCursorReview'] = { 'x': 0, 'y':self.env['screen']['lines'] -1}
        self.env['runtime']['outputManager'].presentText(_("Bottom"), interrupt=True, flush=False)     

    def setCallback(self, callback):
        pass

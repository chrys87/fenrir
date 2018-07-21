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
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'charDeleteEcho'):
            return
        # detect typing or chilling
        if self.env['screen']['newCursor']['x'] >= self.env['screen']['oldCursor']['x']:
            return 

        # More than just a deletion happend
        if self.env['runtime']['screenManager'].isDelta(ignoreSpace=True):
            return

        # no deletion
        if not self.env['runtime']['screenManager'].isNegativeDelta():
            return           

        # too much for a single backspace...
        # word begin produce a diff wiht len == 2 |a | others with 1 |a|
        if len(self.env['screen']['newNegativeDelta']) > 2:
            return
                       
        currNegativeDelta = self.env['screen']['newNegativeDelta']
        if len(currNegativeDelta.strip()) != len(currNegativeDelta) and \
          currNegativeDelta.strip() != '':
            currNegativeDelta = currNegativeDelta.strip()
        self.env['runtime']['outputManager'].presentText(currNegativeDelta, interrupt=True, ignorePunctuation=True, announceCapital=True, flush=False)
    def setCallback(self, callback):
        pass


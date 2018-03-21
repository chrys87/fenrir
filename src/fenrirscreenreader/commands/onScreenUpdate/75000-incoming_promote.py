#!/bin/python
import time
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
        if not self.env['runtime']['settingsManager'].getSettingAsBool('promote', 'enabled'):
            return
        if self.env['runtime']['settingsManager'].getSetting('promote', 'list').strip(" \t\n") == '':
            return
        if int(time.time() - self.env['input']['lastInputTime']) < self.env['runtime']['settingsManager'].getSettingAsInt('promote', 'inactiveTimeoutSec'):
            return
        if len(self.env['runtime']['settingsManager'].getSetting('promote', 'list')) == 0:
            return       
        for promote in self.env['runtime']['settingsManager'].getSetting('promote', 'list').split(','):
            if promote in self.env['screen']['newDelta']:    
                self.env['runtime']['outputManager'].playSoundIcon('PromotedText')        
                self.env['input']['lastInputTime'] = time.time()
                return

    def setCallback(self, callback):
        pass


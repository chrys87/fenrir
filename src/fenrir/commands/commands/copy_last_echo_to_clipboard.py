#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import mark_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('copies last presented text to the currently selected clipboard')    
    
    def run(self):
        lastEcho = self.env['runtime']['outputManager'].getLastEcho()
        self.env['commandBuffer']['clipboard'] = [lastEcho] + self.env['commandBuffer']['clipboard'][:self.env['runtime']['settingsManager'].getSettingAsInt('general', 'numberOfClipboards') -1]
        self.env['commandBuffer']['currClipboard'] = 0
   
        self.env['runtime']['outputManager'].presentText(lastEcho, soundIcon='CopyToClipboard', interrupt=True)

    def setCallback(self, callback):
        pass

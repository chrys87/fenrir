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
        return ''           
    
    def run(self):
        if self.env['runtime']['punctuationManager'].cyclePunctuation():
            self.env['runtime']['outputManager'].presentText(self.env['runtime']['settingsManager'].getSetting('general', 'punctuationLevel'), interrupt=True, ignorePunctuation=True)
        else:
            self.env['runtime']['outputManager'].presentText(_('No punctuation found.'), interrupt=True, ignorePunctuation=True)
            
    def setCallback(self, callback):
        pass

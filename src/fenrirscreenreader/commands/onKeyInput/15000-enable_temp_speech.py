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
        return _('disables speech until next keypress') 
    
    def run(self):
        if self.env['runtime']['inputManager'].noKeyPressed():
            return           
        if len(self.env['input']['prevInput']) >0:
            return
        if not self.env['commandBuffer']['enableSpeechOnKeypress']:
            return
        self.env['runtime']['settingsManager'].setSetting('speech', 'enabled', str(self.env['commandBuffer']['enableSpeechOnKeypress']))
        self.env['commandBuffer']['enableSpeechOnKeypress'] = False
        self.env['runtime']['outputManager'].presentText(_("speech enabled"), soundIcon='SpeechOn', interrupt=True)        
               
    def setCallback(self, callback):
        pass

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
        if self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'enabled'): 
            self.env['runtime']['outputManager'].presentText(_("speech temporary disabled"), soundIcon='SpeechOff', interrupt=True)
            self.env['commandBuffer']['enableSpeechOnKeypress'] = True
            self.env['runtime']['settingsManager'].setSetting('speech', 'enabled', str(not self.env['runtime']['settingsManager'].getSettingAsBool('speech', 'enabled')))
            self.env['runtime']['outputManager'].interruptOutput()            
               
    def setCallback(self, callback):
        pass

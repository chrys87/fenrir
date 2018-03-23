#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import datetime

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('presents the date')        
    
    def run(self):
        dateFormat = self.env['runtime']['settingsManager'].getSetting('general', 'dateFormat')

        # get the time formatted
        dateString = datetime.datetime.strftime(datetime.datetime.now(), dateFormat)

        # present the time via speak and braile, there is no soundicon, interrupt the current speech
        self.env['runtime']['outputManager'].presentText(dateString , soundIcon='', interrupt=True)

    def setCallback(self, callback):
        pass

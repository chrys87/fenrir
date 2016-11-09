#!/bin/python
import time
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import time
import datetime

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.lastTime = time.time()
        self.lastDateString = ''
        self.lastTimeString = ''        
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'     

    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('time', 'enabled'):
            return
        if int(time.time() - self.lastTime) < self.env['runtime']['settingsManager'].getSettingAsInt('time', 'delaySec'):
            return
        timeFormat = self.env['runtime']['settingsManager'].getSetting('general', 'timeFormat')
        timeString = datetime.datetime.strftime(datetime.datetime.now(), timeFormat)
        
        dateFormat = self.env['runtime']['settingsManager'].getSetting('general', 'dateFormat')
        dateString = datetime.datetime.strftime(datetime.datetime.now(), dateFormat)
        if self.env['runtime']['settingsManager'].getSettingAsBool('time', 'presentTime'):
            # present the time
            self.env['runtime']['outputManager'].presentText('Autotime: ' + timeString , soundIcon='', interrupt=False)
        # and date if changes
        if self.env['runtime']['settingsManager'].getSettingAsBool('time', 'presentDate'):        
            if self.lastDateString != dateString:
                self.env['runtime']['outputManager'].presentText(dateString , soundIcon='', interrupt=False)        
                self.lastDateString = dateString
        self.lastTime = time.time() 
        self.lastTimeString = timeString                         
    def setCallback(self, callback):
        pass

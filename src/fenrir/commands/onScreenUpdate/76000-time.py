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
        self.lastTime = datetime.datetime.now()
        self.lastDateString = ''
        self.lastTimeString = ''        
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'     

    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('time', 'enabled'):
            return
        onMinutes = self.env['runtime']['settingsManager'].getSetting('time', 'onMinutes')            
        delaySec = self.env['runtime']['settingsManager'].getSettingAsInt('time', 'delaySec')
        # no need
        if onMinutes == '' and delaySec <= 0:
            return
        onMinutes = onMinutes.split(',')
        now = datetime.datetime.now()
        # ignore onMinutes if there is a delaySec
        if delaySec > 0:
            if int((now-self.lastTime).total_seconds()) < delaySec:
                    return
        else:
            # shoul announce?
            if not str(now.minute) in onMinutes:
                return
            # already announced?
            if now.hour == self.lastTime.hour:
                if now.minute == self.lastTime.minute:
                    return
              
        timeFormat = self.env['runtime']['settingsManager'].getSetting('general', 'timeFormat')
        timeString = datetime.datetime.strftime(now, timeFormat)
        
        dateFormat = self.env['runtime']['settingsManager'].getSetting('general', 'dateFormat')
        dateString = datetime.datetime.strftime(now, dateFormat)
        if self.env['runtime']['settingsManager'].getSettingAsBool('time', 'presentTime'):
            # present the time
            self.env['runtime']['outputManager'].presentText('Autotime: ' + timeString , soundIcon='', interrupt=False)
        # and date if changes
        if self.env['runtime']['settingsManager'].getSettingAsBool('time', 'presentDate'):        
            if self.lastDateString != dateString:
                self.env['runtime']['outputManager'].presentText(dateString , soundIcon='', interrupt=False)        
                self.lastDateString = dateString
        self.lastTime = datetime.datetime.now()
        self.lastTimeString = timeString                         
    def setCallback(self, callback):
        pass

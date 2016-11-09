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

        # get the time formatted
        timeString = datetime.datetime.strftime(datetime.datetime.now(), timeFormat)

        # present the time
        self.env['runtime']['outputManager'].presentText('Autotime: ' + timeString , soundIcon='', interrupt=False)
     
        self.lastTime = time.time()

    def setCallback(self, callback):
        pass


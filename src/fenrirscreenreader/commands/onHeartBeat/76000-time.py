#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
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
            if int((now - self.lastTime).total_seconds()) < delaySec:
                return
        else:
            # should announce?
            if not str(now.minute).zfill(2) in onMinutes:
                return
            # already announced?
            if now.hour == self.lastTime.hour:
                if now.minute == self.lastTime.minute:
                    return

        dateFormat = self.env['runtime']['settingsManager'].getSetting('general', 'dateFormat')
        dateString = datetime.datetime.strftime(now, dateFormat)

        presentDate = self.env['runtime']['settingsManager'].getSettingAsBool('time', 'presentDate') and \
            self.lastDateString != dateString
        presentTime = self.env['runtime']['settingsManager'].getSettingAsBool('time', 'presentTime')

        # no changed value to announce
        if not (presentDate or presentTime):
            return

        timeFormat = self.env['runtime']['settingsManager'].getSetting('general', 'timeFormat')
        timeString = datetime.datetime.strftime(now, timeFormat)

        if self.env['runtime']['settingsManager'].getSettingAsBool('time', 'interrupt'):
            self.env['runtime']['outputManager'].interruptOutput()
        if self.env['runtime']['settingsManager'].getSettingAsBool('time', 'announce'):
            self.env['runtime']['outputManager'].playSoundIcon('announce')

        if presentTime:
            # present the time
            self.env['runtime']['outputManager'].presentText(_("It's {0}").format(timeString.replace(':00', " O'clock ").lstrip('0')), soundIcon='', interrupt=False)
            # Check if it's 12:00 AM
            if now.hour == 0 and now.minute == 0:
                # present the date
                self.env['runtime']['outputManager'].presentText(dateString, soundIcon='', interrupt=False)

        self.lastTime = datetime.datetime.now()
        self.lastTimeString = timeString

    def setCallback(self, callback):
        pass

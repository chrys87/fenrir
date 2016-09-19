#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import datetime

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'presents the time'        

    def run(self, environment):
        timeFormat = environment['runtime']['settingsManager'].getSetting(environment,'general', 'timeFormat')

        # get the time formatted
        timeString = datetime.datetime.strftime(datetime.datetime.now(), timeFormat)

        # present the time via speak and braile, there is no soundicon, interrupt the current speech
        environment['runtime']['outputManager'].presentText(environment, timeString , soundIcon='', interrupt=True)

    def setCallback(self, callback):
        pass

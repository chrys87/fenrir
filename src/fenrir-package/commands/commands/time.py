#!/bin/python

import datetime

class command():
    def __init__(self):
        pass
    def run(self, environment):
        #this is the way to load the settings:
        # general is the section in the config file, timeFormat is the variable
        # this has to been added to settings.conf in sectino [general]
        # timeFormat=%H:%M;%P
        # the following has to been added to core/settings.py to the key 'general'
        # the settings.py is used for default values
        # 'timeFormat':"%H:%M;%P",
        timeFormat = environment['runtime']['settingsManager'].getSetting(environment,'general', 'timeFormat')

        # get the time formatted
        timeString = datetime.datetime.strftime(datetime.datetime.now(), timeFormat)

        # present the time via speak and braile, there is no soundicon, interrupt the current speech
        environment['runtime']['outputManager'].presentText(environment, timeString , soundIcon='', interrupt=True)

        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

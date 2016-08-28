#!/bin/python

import datetime

class command():
    def __init__(self):
        pass
    def run(self, environment):
        #this is the way to load the settings:
        # general is the section in the config file, timeFormat is the variable
        # this has to been added to settings.conf in sectino [general]
        # dateFormat="%A, %B %d, %Y"
        # the following has to been added to core/settings.py to the key 'general'
        # the settings.py is used for default values
        # dateFormat="%A, %B %d, %Y"
        dateFormat = environment['runtime']['settingsManager'].getSetting(environment,'general', 'dateFormat')

        # get the time formatted
        dateString = datetime.datetime.strftime(datetime.datetime.now(), dateFormat)

        # present the time via speak and braile, there is no soundicon, interrupt the current speech
        environment['runtime']['outputManager'].presentText(environment, dateString , soundIcon='', interrupt=True)

        return environment
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

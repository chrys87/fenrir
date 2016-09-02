#!/bin/python

import datetime

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'No Description found'        
    def run(self, environment):
        dateFormat = environment['runtime']['settingsManager'].getSetting(environment,'general', 'dateFormat')

        # get the time formatted
        dateString = datetime.datetime.strftime(datetime.datetime.now(), dateFormat)

        # present the time via speak and braile, there is no soundicon, interrupt the current speech
        environment['runtime']['outputManager'].presentText(environment, dateString , soundIcon='', interrupt=True)

        return environment
    def setCallback(self, callback):
        pass

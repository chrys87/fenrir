#!/bin/python
import time
from utils import debug

class screenManager():
    def __init__(self):

    def initialize(self, environment):
        self.autoIgnoreScreens = []
        if environment['runtime']['settingsManager'].getSettingAsBool(environment,'screen', 'autodetectSuspendingScreen'):
            self.autoIgnoreScreens = environment['runtime']['screenDriver'].getIgnoreScreens()
    def shutdown(self, environment):
        return environment

    def update(self, environment):
        environment['generalInformation']['suspend'] = self.isSuspendingScreen(environment)
        if not environment['generalInformation']['suspend']:
            environment = environment['runtime']['screenDriver'].update(environment)
            environment['screenData']['lastScreenUpdate'] = time.time()
        return environment

    def isSuspendingScreen(self, environment):
        currScreen = environment['runtime']['screenDriver'].getCurrScreen()
        return (currScreen in \
          environment['runtime']['settingsManager'].getSetting(environment,'screen', 'suspendingScreen').split(',')) or
          (currScreen in self.autoIgnoreScreens)


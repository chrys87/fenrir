#!/bin/python
import time
from utils import debug

class screenManager():
    def __init__(self):
        self.autoIgnoreScreens = []

    def initialize(self, environment):
        environment['runtime']['settingsManager'].loadDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'screen', 'driver'), 'screenDriver')    
        if environment['runtime']['settingsManager'].getSettingAsBool(environment,'screen', 'autodetectSuspendingScreen'):
            self.autoIgnoreScreens = environment['runtime']['screenDriver'].getIgnoreScreens()
        return environment
        
    def shutdown(self, environment):
        if environment['runtime']['screenDriver']:
            environment['runtime']['screenDriver'].shutdown(environment)    
        return environment

    def update(self, environment):
        if not self.isSuspendingScreen(environment):
            environment = environment['runtime']['screenDriver'].update(environment)
            environment['screenData']['lastScreenUpdate'] = time.time()
        return environment

    def isSuspendingScreen(self, environment):
        currScreen = environment['runtime']['screenDriver'].getCurrScreen()
        return ((currScreen in \
          environment['runtime']['settingsManager'].getSetting(environment,'screen', 'suspendingScreen').split(',')) or
          (currScreen in self.autoIgnoreScreens))


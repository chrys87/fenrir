#!/bin/python
import time
from utils import debug

class screenManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment
    def update(self, environment):
        environment['generalInformation']['suspend'] = self.isSuspendingScreen(environment)
        if not environment['generalInformation']['suspend']:
            environment = environment['runtime']['screenDriver'].update(environment)
            environment['screenData']['lastScreenUpdate'] = time.time()
        return environment

    def isSuspendingScreen(self, environment):
        return environment['runtime']['screenDriver'].getCurrScreen() in \
          environment['runtime']['settingsManager'].getSetting(environment,'screen', 'suspendingScreen').split(',')


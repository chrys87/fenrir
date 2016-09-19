#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'selects the first clipboard'        
    
    def run(self, environment):
        if len(environment['commandBuffer']['clipboard']) == 0:
            environment['runtime']['outputManager'].presentText(environment, 'clipboard empty', interrupt=True)
            return 
        environment['commandBuffer']['currClipboard'] = 0
        environment['runtime']['outputManager'].presentText(environment, environment['commandBuffer']['clipboard'][environment['commandBuffer']['currClipboard']], interrupt=True)
           
    def setCallback(self, callback):
        pass

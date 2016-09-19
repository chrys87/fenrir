#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import mark_utils

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'copies marked text to the currently selected clipboard'    
    
    def run(self, environment):
        if (environment['commandBuffer']['Marks']['1'] == None) or \
          (environment['commandBuffer']['Marks']['2'] == None):
            environment['runtime']['outputManager'].presentText(environment, "two marks needed", interrupt=True)
            return

        # use the last first and the last setted mark as range
        startMark = environment['commandBuffer']['Marks']['1'].copy()
        if environment['commandBuffer']['Marks']['3'] != None:
            endMark = environment['commandBuffer']['Marks']['3'].copy()    
        else:
            endMark = environment['commandBuffer']['Marks']['2'].copy()         
        marked = mark_utils.getTextBetweenMarks(startMark, endMark, environment['screenData']['newContentText'])

        environment['commandBuffer']['clipboard'] = [marked] + environment['commandBuffer']['clipboard'][:environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'general', 'numberOfClipboards') -1]
        environment['commandBuffer']['currClipboard'] = 0
        # reset marks
        environment['commandBuffer']['Marks']['1'] = None
        environment['commandBuffer']['Marks']['2'] = None
        environment['commandBuffer']['Marks']['3'] = None
        
        if marked.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", soundIcon='EmptyLine', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, marked, interrupt=True)

    def setCallback(self, callback):
        pass

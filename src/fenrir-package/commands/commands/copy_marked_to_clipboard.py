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
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'copies marked text to the currently selected clipboard'    
    
    def run(self):
        if not (self.env['commandBuffer']['Marks']['1'] and \
          self.env['commandBuffer']['Marks']['2']):
            self.env['runtime']['outputManager'].presentText("two marks needed", interrupt=True)
            return
        # use the last first and the last setted mark as range
        startMark = self.env['commandBuffer']['Marks']['1'].copy()
        endMark = self.env['commandBuffer']['Marks']['2'].copy()         
        
        marked = mark_utils.getTextBetweenMarks(startMark, endMark, self.env['screenData']['newContentText'])

        self.env['commandBuffer']['clipboard'] = [marked] + self.env['commandBuffer']['clipboard'][:self.env['runtime']['settingsManager'].getSettingAsInt('general', 'numberOfClipboards') -1]
        self.env['commandBuffer']['currClipboard'] = 0
        # reset marks
        self.env['commandBuffer']['Marks']['1'] = None
        self.env['commandBuffer']['Marks']['2'] = None
        
        if marked.strip(" \t\n") == '':
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(marked, interrupt=True)

    def setCallback(self, callback):
        pass

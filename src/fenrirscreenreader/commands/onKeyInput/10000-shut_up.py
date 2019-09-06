#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        self.smartKeyFilter = ['KEY_SPACE', 'KEY_RETURN', 'KEY_TAB']
    def shutdown(self):
        pass
    def getDescription(self):
        return ''
    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'interruptOnKeyPress'):
            return
        if self.env['runtime']['inputManager'].noKeyPressed():
            return
        if self.env['runtime']['screenManager'].isScreenChange():
            return
        if len(self.env['input']['currInput']) <= len(self.env['input']['prevInput']):
            return
        # if the filter is set
        filterList = []
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'smartInterruptOnKeyPress'):
            filterList = self.env['runtime']['settingsManager'].getSetting('keyboard', 'interruptOnKeyPressFilter').split(',')
        else:
            filterList = self.smartKeyFilter

        if filterList != []:
            found = False
            for currInput in self.env['input']['currInput']:
                print(currInput)
                for filterEntry in filterList:
                    if filterEntry.startswith(currInput):
                        found = True
            if not found:
                return
        self.env['runtime']['outputManager'].interruptOutput()

    def setCallback(self, callback):
        pass

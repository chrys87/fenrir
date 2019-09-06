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
        self.smartByteFilter = [b'\n',b'\t',b' ',b'^']
    def shutdown(self):
        pass
    def getDescription(self):
        return ''
    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'interruptOnKeyPress'):
            return
        if self.env['runtime']['screenManager'].isScreenChange():
            return
        # if the filter is set
        filterList = []
        if not self.env['runtime']['settingsManager'].getSettingAsBool('keyboard', 'smartInterruptOnKeyPress'):
            filterList = self.env['runtime']['settingsManager'].getSetting('keyboard', 'interruptOnKeyPressFilter').split(',')
        else:
            filterList = self.smartByteFilter
            if self.env['runtime']['outputManager'].getOutputReason() != 'char_echo':
                self.env['runtime']['outputManager'].interruptOutput()
        if filterList != []:
            found = False
            for filterEntry in filterList:
                if filterEntry.startswith(self.env['runtime']['byteManager'].getLastByteKey()):
                    found = True
            if not found:
                return
        self.env['runtime']['outputManager'].interruptOutput()

    def setCallback(self, callback):
        pass

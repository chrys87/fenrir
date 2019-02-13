#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class quickMenuManager():
    def __init__(self):
        self.position = 0
        self.quickMenu = []
    def initialize(self, environment):
        self.env = environment
        self.loadMenu(self.env['runtime']['settingsManager'].getSetting('menu', 'quickMenu'))
    def shutdown(self):
        pass
    def loadMenu(self, menuString):
        self.position = 0
        self.quickMenu = []
        if menuString == '':
            return
        entrys = menuString.split(';')
        for e in entrys:
            entry = e.split('#')
            if len(entry) != 2:
                continue
            self.quickMenu.append({'section': entry[0], 'setting': entry[1]})
    def nextEntry(self):
        if len(self.quickMenu) == 0:
            return False
        self.position += 1
        if self.position >= len(self.quickMenu):
            self.position = 0
        return True
    def prevEntry(self):
        if len(self.quickMenu) == 0:
            return False
        self.position -= 1
        if self.position < 0:
            self.position = len(self.quickMenu) - 1
        return True
    def nextValue(self):
        if len(self.quickMenu) == 0:
            return False
        try:
            valueString = self.env['runtime']['settingsManager'].getSetting(self.quickMenu[self.position]['section'], self.quickMenu[self.position]['setting'])
        except:
            return False
        # bool
        if valueString.upper() in ['TRUE', 'FALSE']:
            value = valueString.upper() == 'TRUE'
            value = not value
            self.env['runtime']['settingsManager'].setSettingAsBool(self.quickMenu[self.position]['section'], self.quickMenu[self.position]['setting'], value)
            return True
        # float
        try:
            value = float(valueString)
            value += 0.05
            if value > 1.0:
                value = 1.0
            self.env['runtime']['settingsManager'].setSettingAsFloat(self.quickMenu[self.position]['section'], self.quickMenu[self.position]['setting'], value)
            return True
        except:
            pass
        return True
    def prevValue(self):
        if len(self.quickMenu) == 0:
            return False
        try:
            valueString = self.env['runtime']['settingsManager'].getSetting(self.quickMenu[self.position]['section'], self.quickMenu[self.position]['setting'])
        except:
            return False
        # bool
        if valueString.upper() in ['TRUE', 'FALSE']:
            value = valueString.upper() == 'TRUE'
            value = not value
            self.env['runtime']['settingsManager'].setSettingAsBool(self.quickMenu[self.position]['section'], self.quickMenu[self.position]['setting'], value)
            return True
        # float
        try:
            value = float(valueString)
            value -= 0.05
            if value < 0.0:
                value = 0
            self.env['runtime']['settingsManager'].setSettingAsFloat(self.quickMenu[self.position]['section'], self.quickMenu[self.position]['setting'], value)
            return True
        except:
            pass
        return True
    def getCurrentEntry(self):
        if len(self.quickMenu) == 0:
            return ''
        try:
            return _(self.quickMenu[self.position]['section']) + ' ' + _(self.quickMenu[self.position]['setting'])
        except:
            return _('setting invalid')
    def getCurrentValue(self):
        if len(self.quickMenu) == 0:
            return ''
        try:
            return self.env['runtime']['settingsManager'].getSetting(self.quickMenu[self.position]['section'], self.quickMenu[self.position]['setting'])
        except:
            return _('setting value invalid')


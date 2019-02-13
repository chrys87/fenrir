#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.settingsData import settingsData

class quickMenuManager():
    def __init__(self):
        self.position = 0
        self.quickMenu = []
        self.settings = settingsData

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
            try:
                t = self.settings[entry[0]][entry[1]]
            except:
                print(entry[0],entry[1], 'not found')
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
        section = self.quickMenu[self.position]['section']
        setting = self.quickMenu[self.position]['setting']
        valueString = ''
        try:
            valueString = self.env['runtime']['settingsManager'].getSetting(section, setting)
        except:
            return False

        try:
            if isinstance(self.settings[section][setting], str):
                value = str(valueString)
                return False
            elif isinstance(self.settings[section][setting], bool):
                if not valueString in ['True','False']:
                    return False
                value = not value
                self.env['runtime']['settingsManager'].setSetting(section, setting, str(value))
            elif isinstance(self.settings[section][setting], int):
                value = int(valueString)
                value += 1
                self.env['runtime']['settingsManager'].setSetting(section, setting, str(value))
            elif isinstance(self.settings[section][setting], float):
                value = float(valueString)
                value += 0.05
                if value > 1.0:
                    value = 1.0
                self.env['runtime']['settingsManager'].setSetting(section, setting, str(value)[:4])
        except Exception as e:
            return False
        return True
    def prevValue(self):
        if len(self.quickMenu) == 0:
            return False
        section = self.quickMenu[self.position]['section']
        setting = self.quickMenu[self.position]['setting']
        valueString = ''
        try:
            valueString = self.env['runtime']['settingsManager'].getSetting(section, setting)
        except:
            return False
        try:
            if isinstance(self.settings[section][setting], str):
                value = str(valueString)
                return False
            elif isinstance(self.settings[section][setting], bool):
                if not valueString in ['True','False']:
                    return False
                value = not value
                self.env['runtime']['settingsManager'].setSetting(section, setting, str(value))
            elif isinstance(self.settings[section][setting], int):
                value = int(valueString)
                value -= 1
                if value < 0:
                    value = 0
                self.env['runtime']['settingsManager'].setSetting(section, setting, str(value))
            elif isinstance(self.settings[section][setting], float):
                value = float(valueString)
                value -= 0.05
                if value < 0.0:
                    value = 0.0
                self.env['runtime']['settingsManager'].setSetting(section, setting, str(value)[:4])
        except Exception as e:
            return False
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

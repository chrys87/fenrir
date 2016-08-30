#!/usr/bin/python
# Debugger module for the Fenrir screen reader.

from enum import Enum

class debugLevel(Enum):
    DEACTIVE = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    def __int__(self):
        return self.value

class debug():
    def __init__(self,  fileName='/var/log/fenrir.log'):
        self._fileName = fileName
        self._file = None
        self._fileOpened = False

    def __del__(self):
        try:
            self.closeDebugFile()
        except:
            pass

    def openDebugFile(self, fileName = ''):
        self._fileOpened = False
        if fileName != '':
            self._fileName = fileName
        if self._fileName != '':
            self._file = open(self._fileName,'a')
            self._fileOpened = True

    def writeDebugOut(self, environment, text, level = debugLevel.DEACTIVE):
        if environment['runtime']['settingsManager'].getSettingAsInt(environment, 'general','debugLevel') < int(level):
            if self._fileOpened:
                self.closeDebugFile()
            return
        else:
            if not self._fileOpened:
                self.openDebugFile()
            self._file.write(text + '\n')

    def closeDebugFile(self):
        if not self._fileOpened:
            return False
        if self._file != None:
            self._file.close()
        self._fileOpened = False
        return True

    def getDebugFile(self):
        return self._fileName

    def setDebugFile(self, fileName):
        self.closeDebugFile()
        self._fileName = fileName




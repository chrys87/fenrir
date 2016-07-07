#!/usr/bin/python

# Debugger module for the Fenrir screen reader.

ERROR = 0
WARNING = 1
INFO = 2

class debug():
    def __init__(self,  fileName='/var/log/fenrir.log', level = ERROR):
        self._level = level
        self._fileName= fileName
        self._file = open(self._fileName,'w')
        self._fileOpened = True

    def openDebugFile(self, fileName = ''):
        if fileName != '':
            self._fileName = fileName
        if self._fileName != '':
            self.file = open(self._fileName,'w')
            self._fileOpened = True

    def writeLog(self, text, level = ERROR):
        if not self._fileOpened:
            return False
        if self._level < level:
            return False
        self._file.write(text + '\n')
        return True

    def closeDebugFile(self):
        if not self._fileOpened:
            return False
        self._file.close()
        self._fileOpened = False
        return True
        
    def getDebugLevel(self):
        return self._level

    def setDebugLevel(self, level):
        self._level = level

    def getDebugFile(self):
        return self._fileName

    def setDebugFile(self, fileName):
        self._fileName = fileName



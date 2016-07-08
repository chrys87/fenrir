#!/usr/bin/python

# Debugger module for the Fenrir screen reader.

DEACTIVE = 0
ERROR = 1
WARNING = 2
INFO = 3

class debug():
    def __init__(self,  fileName='/var/log/fenrir.log', level = DEACTIVE):
        self._level = level
        self._fileName = fileName
        self._file = ''
        self._fileOpened = False

    def openDebugFile(self, fileName = ''):
        self._fileOpened = False
        if fileName != '':
            self._fileName = fileName
        if self._fileName != '':
            self.file = open(self._fileName,'w')
            self._fileOpened = True

    def writeDebugOut(self, envirionment, text, level = DEACTIVE):
        if self._level < level:
            if self._fileOpened:
                self.closeDebugFile()
            return
        else:
            if not self._fileOpened:
                self.openDebugFile()
            self.writeLog(environment, text, level):

    def writeLog(self, environment, text, level:
        if self._level < level:
            return False
        if not self._fileOpened:
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
        self.closeDebugFile()
        if self._fileOpened:
           self.openDebugFile(self, fileName):




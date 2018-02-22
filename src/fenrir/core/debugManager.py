#!/usr/bin/python
# Debugger module for the Fenrir screen reader.

from core import debug
from datetime import datetime

class debugManager():
    def __init__(self,  fileName='/var/log/fenrir.log'):
        self._fileName = fileName
        self._file = None
        self._fileOpened = False
    def initialize(self, environment):
        self.env = environment    
    def shutdown(self):
        self.closeDebugFile()
    def __del__(self):
        try:
            self.shutdown()
        except:
            pass

    def openDebugFile(self, fileName = ''):
        self._fileOpened = False
        if fileName != '':
            self._fileName = fileName
        if self._fileName != '':
            self._file = open(self._fileName,'a')
            self._fileOpened = True

    def writeDebugOut(self, text, level = debug.debugLevel.DEACTIVE, onAnyLevel=False):
    
        mode = self.env['runtime']['settingsManager'].getSetting('general','debugMode')
        if mode == '':
            mode = 'FILE' 
        mode = mode.upper().split(',')
        fileMode = 'FILE' in mode
        printMode = 'PRINT' in mode
              
        if (self.env['runtime']['settingsManager'].getSettingAsInt('general','debugLevel') < int(level)) and \
        not (onAnyLevel and self.env['runtime']['settingsManager'].getSettingAsInt('general','debugLevel') > int(debug.debugLevel.DEACTIVE)) :
            if self._fileOpened:
                self.closeDebugFile()
            return
        else:
            if not self._fileOpened and fileMode:
                self.openDebugFile()
            if onAnyLevel:
                msg = 'ANY '+ str(level) + ' ' +  str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'))
            else:            
                msg = str(level) +' ' + str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
)
            msg +=  ': ' + text         
            if printMode:
                print(msg)
            if fileMode:
                self._file.write(msg + '\n')            

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

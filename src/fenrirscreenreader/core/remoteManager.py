#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

'''
Remote controll:
section<space>command<space>parameters
sections:command,setting
setting commands:
- set section#setting=value[;section#setting=value]
- reset
command commands:
- say text to speech
- interrupt
examples
settings:
settings set section#setting=value[,section#setting=value]
setting set speech#voice=de
setting reset
setting save /path/settings.conf
command:
command say this is a test
command interrupt
'''


from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType
import time, os

class remoteManager():
    def __init__(self):
        # command controll
        self.commandConst = 'COMMAND '
        self.sayConst = 'SAY '
        self.vmenuConst = 'VMENU '
        self.resetVmenuConst = 'RESETVMENU'
        self.interruptConst = 'INTERRUPT'
        self.quitAppConst = 'QUITAPPLICATION'
        self.tempDisableSpeechConst = 'TEMPDISABLESPEECH'
        self.defineWindowConst = 'WINDOW '
        self.resetWindowConst = 'RESETWINDOW'
        self.setClipboardConst = 'CLIPBOARD '
        self.exportClipboardConst = 'EXPORTCLIPBOARD'
        # setting controll
        self.settingConst = 'SETTING '
        self.setSettingConst = 'SET '
        self.saveAsSettingConst = 'SAVEAS '
        self.saveSettingConst = 'SAVE'
        self.resetSettingConst = 'RESET'
    def initialize(self, environment):
        self.env = environment
        self.env['runtime']['settingsManager'].loadDriver(\
          self.env['runtime']['settingsManager'].getSetting('remote', 'driver'), 'remoteDriver')
    def shutdown(self):
        self.env['runtime']['settingsManager'].shutdownDriver('remoteDriver')

    def handleSettingsChange(self, settingsText):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('remote', 'enableSettingsRemote'):
            return

        upperSettingsText = settingsText.upper()
        # set setting
        if upperSettingsText.startswith(self.setSettingConst):
            parameterText = settingsText[len(self.setSettingConst):]
            self.setSettings(parameterText)
        # save as setting
        elif upperSettingsText.startswith(self.saveAsSettingConst):
            parameterText = settingsText[len(self.saveAsSettingConst):]
            self.saveSettings(parameterText)
        # save setting
        elif upperSettingsText == self.saveSettingConst:
            self.saveSettings()
        # reset setting
        elif upperSettingsText == self.resetSettingConst:
            self.resetSettings()

    def handleCommandExecution(self, commandText):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('remote', 'enableCommandRemote'):
            return

        upperCommandText = commandText.upper()

        # say
        if upperCommandText.startswith(self.sayConst):
            parameterText = commandText[len(self.sayConst):]
            self.say(parameterText)
        # interrupt
        elif upperCommandText == self.interruptConst:
            self.interruptSpeech()
        # temp disable speech
        elif upperCommandText == self.tempDisableSpeechConst:
            self.tempDisableSpeech()
        # set vmenu
        elif upperCommandText.startswith(self.vmenuConst):
            parameterText = commandText[len(self.vmenuConst):]
            self.setVMenu(parameterText)
        # reset vmenu
        elif upperCommandText == self.resetVmenuConst:
            self.resetVMenu()
        # quit fenrir
        elif upperCommandText == self.quitAppConst:
            self.quitFenrir()
        # define window
        elif upperCommandText.startswith(self.defineWindowConst):
            parameterText = commandText[len(self.defineWindowConst):]
            self.defineWindow(parameterText)
        # reset window
        elif upperCommandText == self.resetWindowConst:
            self.resetWindow()
        # set clipboard
        elif upperCommandText.startswith(self.setClipboardConst):
            parameterText = commandText[len(self.setClipboardConst):]
            self.setClipboard(parameterText)
        elif upperCommandText.startswith(self.exportClipboardConst):
            self.exportClipboard()
    def tempDisableSpeech(self):
        self.env['runtime']['outputManager'].tempDisableSpeech()
    def setVMenu(self, vmenu = ''):
        self.env['runtime']['vmenuManager'].setCurrMenu(vmenu)
    def resetVMenu(self):
        self.env['runtime']['vmenuManager'].setCurrMenu()
    def setClipboard(self, text = ''):
        self.env['runtime']['memoryManager'].addValueToFirstIndex('clipboardHistory', text)
    def quitFenrir(self):
        self.env['runtime']['eventManager'].stopMainEventLoop()
    def defineWindow(self, windowText):
        start = {}
        end = {}
        try:
            windowList = windowText.split(' ')
            if len(windowList) < 4:
                return
            start['x'] = int(windowList[0])
            start['y'] = int(windowList[1])
            end['x'] = int(windowList[2])
            end['y'] = int(windowList[3])

            self.env['runtime']['cursorManager'].setWindowForApplication(start, end)
        except Exception as e:
            pass
    def resetWindow(self):
        self.env['runtime']['cursorManager'].clearWindowForApplication()
    def say(self, text):
        if not text:
            return
        if text == '':
            return
        self.env['runtime']['outputManager'].speakText(text)
    def interruptSpeech(self):
        self.env['runtime']['outputManager'].interruptOutput()
    def exportClipboard(self):
        clipboardFilePath = self.env['runtime']['settingsManager'].getSetting('general', 'clipboardExportPath')
        clipboardFilePath = clipboardFilePath.replace('$user',self.env['general']['currUser'])
        clipboardFilePath = clipboardFilePath.replace('$USER',self.env['general']['currUser'])
        clipboardFilePath = clipboardFilePath.replace('$User',self.env['general']['currUser'])
        clipboardFile = open(clipboardFilePath,'w')
        try:
            if self.env['runtime']['memoryManager'].isIndexListEmpty('clipboardHistory'):
                self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
                return 
            clipboard = self.env['runtime']['memoryManager'].getIndexListElement('clipboardHistory')
            # Fenrir will crash if the clipboard variable is type None
            if clipboard is not None:
                clipboardFile.write(clipboard)
            else:
                clipboardFile.write('')
            clipboardFile.close()
            os.chmod(clipboardFilePath, 0o666)
            self.env['runtime']['outputManager'].presentText(_('clipboard exported to file'), interrupt=True)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('export_clipboard_to_file:run: Filepath:'+ clipboardFile +' trace:' + str(e),debug.debugLevel.ERROR)    
    
    def saveSettings(self, settingConfigPath = None):
        if not settingConfigPath:
            settingConfigPath = self.env['runtime']['settingsManager'].getSettingsFile()
        if settingConfigPath == '':
            return
        self.env['runtime']['settingsManager'].saveSettings(settingConfigPath)
    def resetSettings(self):
        self.env['runtime']['settingsManager'].resetSettingArgDict()
    def setSettings(self, settingsArgs):
        self.env['runtime']['settingsManager'].parseSettingArgs(settingsArgs)
        self.env['runtime']['screenManager'].updateScreenIgnored()
        self.env['runtime']['inputManager'].handleDeviceGrab(force = True)
    def handleRemoteIncomming(self, eventData):
        if not eventData:
            return
        upperEventData = eventData.upper()
        self.env['runtime']['debug'].writeDebugOut('remoteManager:handleRemoteIncomming: event: ' + str(eventData),debug.debugLevel.INFO)

        if upperEventData.startswith(self.settingConst):
            settingsText = eventData[len(self.settingConst):]
            self.handleSettingsChange(settingsText)
        elif upperEventData.startswith(self.commandConst):
            commandText = eventData[len(self.commandConst):]
            self.handleCommandExecution(commandText)

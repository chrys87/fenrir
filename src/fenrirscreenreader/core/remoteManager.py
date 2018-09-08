#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

'''
Remote controll:
section<space>command<space>parameters
sections:command,setting
setting commands:
- set section#setting=value[,section#setting=value]
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
import time
import select
import socket
import os, os.path, sys, stat

class remoteManager():
    def __init__(self):
        # command controll
        self.commandConst = 'COMMAND '
        self.sayConst = 'SAY '
        self.interruptConst = 'INTERRUPT'
        self.defineWindowConst = 'WINDOW '
        self.resetWindowConst = 'RESETWINDOW'
        # setting controll
        self.settingConst = 'SETTING '
        self.setSettingConst = 'SET '
        self.saveSettingConst = 'SAVE '
        self.resetSettingConst = 'RESET'
    def initialize(self, environment):
        self.env = environment

        if self.env['runtime']['settingsManager'].getSettingAsBool('remote', 'enabled'):
            if self.env['runtime']['settingsManager'].getSetting('remote', 'method').upper() == 'UNIX':
                self.env['runtime']['processManager'].addCustomEventThread(self.unixSocketWatchDog, multiprocess=True)
            elif self.env['runtime']['settingsManager'].getSetting('remote', 'method').upper() == 'TCP':
                self.env['runtime']['processManager'].addCustomEventThread(self.tcpWatchDog, multiprocess=True)
    def shutdown(self):
        if self.sock:
            self.sock.close()
            self.sock = None
    def unixSocketWatchDog(self, active, eventQueue):
        # echo "command say this is a test" | socat - UNIX-CLIENT:/tmp/fenrirscreenreader-deamon.sock

        if self.env['runtime']['settingsManager'].getSetting('screen', 'driver') =='vcsaDriver':
            socketpath = self.env['runtime']['settingsManager'].getSettingAsInt('remote', 'socketpath') + 'fenrirscreenreader-deamon.sock'
        else:
            socketpath = self.env['runtime']['settingsManager'].getSettingAsInt('remote', 'socketpath') + 'fenrirscreenreader-' + str(os.getpid()) + '.sock'
        if os.path.exists(socketpath):
            os.remove(socketpath)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(socketpath)
        self.sock.listen(1)
        if self.env['runtime']['settingsManager'].getSetting('screen', 'driver') =='vcsaDriver':
            os.chmod(socketpath, 0o222)
        while active.value == 1:
            client_sock, client_addr = self.sock.accept()
            if client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    r, w, e = select.select([client_sock,], [], [])
                except select.error:
                    return
                if len(r) > 0:
                    rawdata = client_sock.recv(8129)
                    try:
                        data = rawdata.decode("utf-8").rstrip().lstrip()
                        eventQueue.put({"Type":fenrirEventType.RemoteIncomming,
                            "Data": data
                        })
                    except:
                        pass
                client_sock.close()

        if os.path.exists(socketpath):
            os.remove(socketpath)
        if self.sock:
            self.sock.close()
            self.sock = None
    def tcpWatchDog(self, active, eventQueue):
        # echo "command say this is a test" | nc localhost 22447
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = '127.0.0.1'
        self.port = self.env['runtime']['settingsManager'].getSettingAsInt('remote', 'port')
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        while active.value == 1:
            client_sock, client_addr = self.sock.accept()
            if client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    r, w, e = select.select([client_sock,], [], [])
                except select.error:
                    return
                if len(r) > 0:
                    rawdata = client_sock.recv(8129)
                    try:
                        data = rawdata.decode("utf-8").rstrip().lstrip()
                        eventQueue.put({"Type":fenrirEventType.RemoteIncomming,
                            "Data": data
                        })
                    except:
                        pass
                client_sock.close()
        if self.sock:
            self.sock.close()
            self.sock = None
    def handleSettingsChange(self, settingsText):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('remote', 'enableSettingsRemote'):
            return

        upperSettingsText = settingsText.upper()
        # set setting
        if upperSettingsText.startswith(self.setSettingConst):
            parameterText = settingsText[len(self.setSettingConst):]
            self.setSettings(parameterText)
        # save setting
        if upperSettingsText.startswith(self.saveSettingConst):
            parameterText = settingsText[len(self.saveSettingConst):]
            self.saveSettings(parameterText)
        # reset setting
        if upperSettingsText.startswith(self.resetSettingConst):
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
        if upperCommandText.startswith(self.interruptConst):
            self.interruptSpeech()
        # define window
        if upperCommandText.startswith(self.defineWindowConst):
            parameterText = commandText[len(self.defineWindowConst):]
            self.defineWindow(parameterText)
        # reset window
        if upperCommandText.startswith(self.resetWindowConst):
            self.resetWindow()
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
    def saveSettings(self, settingConfigPath):
        if not settingConfigPath:
            return
        if settingConfigPath == '':
            return
        self.env['runtime']['settingsManager'].saveSettings(settingConfigPath)
    def resetSettings(self):
        self.env['runtime']['settingsManager'].resetSettingArgDict()
    def setSettings(self, settingsArgs):
        self.env['runtime']['settingsManager'].parseSettingArgs(settingsArgs)
    def handleRemoteIncomming(self, eventData):
        if not eventData:
            return
        upperEventData = eventData.upper()
        if upperEventData.startswith(self.settingConst):
            settingsText = eventData[len(self.settingConst):]
            self.handleSettingsChange(settingsText)
        elif upperEventData.startswith(self.commandConst):
            commandText = eventData[len(self.commandConst):]
            self.handleCommandExecution(commandText)

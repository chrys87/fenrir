#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType
import time
import select
import socket
import os, os.path

class remoteManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment

        if self.env['runtime']['settingsManager'].getSettingAsBool('remote', 'enabled'):
            if self.env['runtime']['settingsManager'].getSetting('remote', 'method') == 'unix':
                self.env['runtime']['processManager'].addCustomEventThread(self.unixSocketWatchDog, multiprocess=True)
            elif self.env['runtime']['settingsManager'].getSetting('remote', 'method') == 'tcp':
                self.env['runtime']['processManager'].addCustomEventThread(self.tcpWatchDog, multiprocess=True)
    def shutdown(self):
        if self.sock:
            self.sock.close()
            self.sock = None
    def unixSocketWatchDog(self, active, eventQueue):
        # echo "#<=>#command##exec#say##this is a test" | socat - UNIX-CLIENT:/tmp/fenrir-deamon.sock
        if os.path.exists("/tmp/fenrir-deamon.sock"):
            os.remove("/tmp/fenrir-deamon.sock")
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)            
        self.sock.bind("/tmp/fenrir-deamon.sock")
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
                        data = rawdata.decode("utf-8").rstrip()
                        if data.startswith('#<=>#'):
                            eventQueue.put({"Type":fenrirEventType.RemoteIncomming,
                                "Data": data
                            })
                    except:
                        pass
                client_sock.close()
        if self.sock:
            self.sock.close()
            self.sock = None
    def tcpWatchDog(self, active, eventQueue):
        # echo "#<=>#command##exec#say##this is a test" | nc localhost 22447
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = '0.0.0.0'
        self.port = 22447
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
                        data = rawdata.decode("utf-8").rstrip()
                        if data.startswith('#<=>#'):
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
        if settingsText.startswith('set##'):
            parameterText = settingsText[len('set##'):]
            self.setSettings(parameterText)
        if settingsText.startswith('reset'):
            self.resetSettings()
    def handleCommandExecution(self, commandText):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('remote', 'enableCommandRemote'):
            return
        if commandText.startswith('exec#say##'):
            parameterText = commandText[len('exec#say##'):]
            self.execSay(parameterText)
        if commandText.startswith('cancel##say'):
            self.execInterruptSpeech()
    def execSay(self, text):
        self.env['runtime']['outputManager'].speakText(text)
    def execInterruptSpeech(self):
        self.env['runtime']['outputManager'].interruptOutput()
    def resetSettings(self):
        self.env['runtime']['settingsManager'].resetSettingArgDict()
    def setSettings(self, settingsArgs):
        self.env['runtime']['settingsManager'].parseSettingArgs(settingsArgs)
    def handleRemoteIncomming(self, eventData):
        if not eventData:
            return
        # settings:
        # #<=>#settings##set##section#setting=value[,section#setting=value]
        # #<=>#settings##set##speech#voice=de
        # #<=>#settings##reset
        # execute command:
        # #<=>#command##exec#say##this is a test
        # #<=>#command##cancel##say
        if not eventData.startswith('#<=>#'):
            return
        if eventData.startswith('#<=>#settings##'):
            settingsText = eventData[len('#<=>#settings##'):]
            self.handleSettingsChange(settingsText)
        elif eventData.startswith('#<=>#command##'):
            commandText = eventData[len('#<=>#command##'):]
            self.handleCommandExecution(commandText)

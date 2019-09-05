#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.remoteDriver import remoteDriver
from fenrirscreenreader.core.eventData import fenrirEventType

import select, socket, os, os.path

class driver(remoteDriver):
    def __init__(self):
        remoteDriver.__init__(self)
    def initialize(self, environment):
        self.env = environment    
        self.env['runtime']['processManager'].addCustomEventThread(self.watchDog, multiprocess=True)
    def watchDog(self, active, eventQueue):
        # echo "command say this is a test" | nc localhost 22447
        self.fenrirSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fenrirSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = '127.0.0.1'
        self.port = self.env['runtime']['settingsManager'].getSettingAsInt('remote', 'port')
        self.fenrirSock.bind((self.host, self.port))
        self.fenrirSock.listen(1)
        while active.value:
            try:
                r, _, _ = select.select([self.fenrirSock], [], [], 0.8)
            except select.error:
                break
            if r == []:
                continue
            if self.fenrirSock in r:
                client_sock, client_addr = self.fenrirSock.accept()
            try:
                rawdata = client_sock.recv(8129)
            except:
                pass
            try:
                data = rawdata.decode("utf-8").rstrip().lstrip()
                eventQueue.put({"Type":fenrirEventType.RemoteIncomming,
                    "Data": data
                })
            except:
                pass
            try:
                client_sock.close()
            except:
                pass
        if self.fenrirSock:
            self.fenrirSock.close()
            self.fenrirSock = None

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
        # echo "command say this is a test" | socat - UNIX-CLIENT:/tmp/fenrirscreenreader-deamon.sock
        socketFile = ''
        try:
            socketFile = self.env['runtime']['settingsManager'].getSetting('remote', 'socketFile')
        except:
            pass
        if socketFile == '':
            if self.env['runtime']['settingsManager'].getSetting('screen', 'driver') =='vcsaDriver':
                socketFile =  '/tmp/fenrirscreenreader-deamon.sock'
            else:
                socketFile = '/tmp/fenrirscreenreader-' + str(os.getppid()) + '.sock'
        if os.path.exists(socketFile):
            os.unlink(socketFile)
        self.fenrirSock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.fenrirSock.bind(socketFile)
        os.chmod(socketFile, 0o222)
        self.fenrirSock.listen(1)
        while active.value:
            # Check if the client is still connected and if data is available:
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
        if os.path.exists(socketFile):
            os.unlink(socketFile)
